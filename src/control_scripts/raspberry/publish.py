from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
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

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def get_Host_name_IP():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return host_name,host_ip
    
# Read in command-line parameters

host = "a1pdiz5spt6eed-ats.iot.us-east-2.amazonaws.com"
rootCAPath = "/home/pi/certificates/AmazonRootCA1.pem"
certificatePath = "/home/pi/certificates/f06dbeafe6ea77bcfc740190ba19a00511ddb31c58c7decc9def95e7b9f06b0c-certificate.pem.crt"
privateKeyPath = "/home/pi/certificates/f06dbeafe6ea77bcfc740190ba19a00511ddb31c58c7decc9def95e7b9f06b0c-private.pem.key"
port = 8883
clientId = "webapp"
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

message = {}
message["message"]="hello"
state={}
    

state["reported"]={}
state['reported']["time"] = str(datetime.datetime.now())
state['reported']["threshold"] = 50
state['reported']["ip"] =ip
state['reported']["local_host"] =local_host
message["state"]=state
messageJson=json.dumps(message)
myAWSIoTMQTTClient.publish(topic,messageJson,1)

print('Published topic %s: %s\n' % (topic, messageJson))
time.sleep(2)

import time

currentTime = time.strftime("%H:%M:%S", time.localtime()) 
print(currentTime)
print(type(currentTime))
