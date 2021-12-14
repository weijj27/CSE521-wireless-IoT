from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO  
import logging
import time
import argparse
import json
import socket
import datetime
import random
import sys
import os
AllowedActions = ['both', 'publish', 'subscribe']
LUMIN = 0
THRESHOLD = -1
LOCATION = 0
MORING = "DEFAULT"
EVENING = "DEFAULT"
in1 = 23
in2 = 24
ena = 25
# Custom MQTT message callback
def customCallback(client, userdata, message):
    global MORING,EVENING,THRESHOLD,LUMIN,in1,in2,ena
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    received = eval(message.payload)
    try:
        THRESHOLD = received["state"]["reported"]["threshold"]
        print("*****************************************")
        print(THRESHOLD)
        print("*****************************************")
    except:
        print("No New threshold message coming in.")
        print("current threshold:" + str(THRESHOLD))
        print("current lumin:" + str(LUMIN))

    try:
        MORING = received["state"]["reported"]["opentime"]
        print("*****************************************")
        print("New open time: " +MORING)
        print("*****************************************")
    except:
        print("current open time: " + MORING)
    
    try:
        EVENING = received["state"]["reported"]["closetime"]
        print("*****************************************")
        print("New close time: " +EVENING)
        print("*****************************************")
    except:
        print("current close time: " + EVENING)
    
def get_Host_name_IP():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return host_name,host_ip

def setupMotor(in1,in2,ena):   
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(ena,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    p=GPIO.PWM(ena,1000)
    p.start(25)
    return p


# Read in command-line parameters

host = "a1pdiz5spt6eed-ats.iot.us-east-2.amazonaws.com"
rootCAPath = "/home/pi/certificates/AmazonRootCA1.pem"
certificatePath = "/home/pi/certificates/f06dbeafe6ea77bcfc740190ba19a00511ddb31c58c7decc9def95e7b9f06b0c-certificate.pem.crt"
privateKeyPath = "/home/pi/certificates/f06dbeafe6ea77bcfc740190ba19a00511ddb31c58c7decc9def95e7b9f06b0c-private.pem.key"
port = 8883
clientId = "rasp"
topic = "$aws/things/rasp/shadow/name/raspberry_lumin/update"



# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
local_host,ip=get_Host_name_IP()


libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_TSL2591 import TSL2591

logging.basicConfig(level=logging.INFO)

sensor = TSL2591.TSL2591()
p=setupMotor(in1,in2,ena)


while True:
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    message = {}
    message["message"]="hello"
    state={}
    lux = sensor.Lux
    state["reported"]={}
    state['reported']["time"] = str(datetime.datetime.now())
    state['reported']["lumin"] = lux
    state['reported']["ip"] =ip
    state['reported']["local_host"] =local_host
    currentTime = time.strftime("%H:%M", time.localtime())
    print(currentTime)
    print(EVENING)
    if currentTime == EVENING:
        state['reported']["threshold"] =-1
    if currentTime == MORING:
        state['reported']["threshold"] = 20000
        
    state['reported']["local_host"] 
    message["state"]=state
    messageJson=json.dumps(message)
    LUMIN = lux
    difference = 50
    if not isinstance(THRESHOLD,float):
        THRESHOLD = float(THRESHOLD)
    if not isinstance(LUMIN,float):
        LUMIN = float(LUMIN)
    if LUMIN > (THRESHOLD+difference) and THRESHOLD > 0 and LOCATION > 0:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        p.ChangeDutyCycle(70)
        time.sleep(0.1)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        LOCATION -= 1
        
    if LUMIN < (THRESHOLD-difference) and THRESHOLD > 0 and LOCATION < 10:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        p.ChangeDutyCycle(70)
        time.sleep(0.1)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        LOCATION += 1
    if THRESHOLD == -1:
        while LOCATION>0:
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            p.ChangeDutyCycle(70)
            time.sleep(0.1)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            LOCATION -= 1
    if THRESHOLD == 20000:
        while LOCATION<10:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            p.ChangeDutyCycle(70)
            time.sleep(0.1)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            LOCATION += 1
    try:
        myAWSIoTMQTTClient.publish(topic,messageJson,1)
        print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        time.sleep(1)
    except:
        print("Time out, try again")
        time.sleep(5)
