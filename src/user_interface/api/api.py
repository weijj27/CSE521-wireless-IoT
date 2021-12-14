# coding=utf-8
from flask import Flask
#from flask_mysqldb import MySQL
from flask import request
from flask import jsonify
import datetime
import time
import math
import random
import chardet
import json
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import argparse
import json
import socket
import os
AllowedActions = ['both', 'publish', 'subscribe']
app = Flask(__name__)

# School Page information
param_diction = {}
#mysql = MySQL(app)
M={"state":{"reported":{"lumin":-1}}}
temp=-1

host = "a1pdiz5spt6eed-ats.iot.us-east-2.amazonaws.com"
rootCAPath = "/home/crazenbunny/pi/certificates/AmazonRootCA1.pem"
certificatePath = "/home/crazenbunny/pi/certificates/f06dbeafe6ea77bcfc740190ba19a00511ddb31c58c7decc9def95e7b9f06b0c-certificate.pem.crt"
privateKeyPath = "/home/crazenbunny/pi/certificates/f06dbeafe6ea77bcfc740190ba19a00511ddb31c58c7decc9def95e7b9f06b0c-private.pem.key"
port = 8883
clientId = "webapp"
topic = "$aws/things/rasp/shadow/name/raspberry_lumin/update"


def customCallback(client, userdata, message):
    global M
    print("Received a new message: ")
    print(message.payload)
    M=eval(message.payload.decode("utf-8"))
    print("--------------\n\n")
    print(type(M))
    print("--------------\n\n")
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def get_Host_name_IP():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return host_name,host_ip

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

myAWSIoTMQTTClient.connect()
local_host,ip=get_Host_name_IP()




@app.route('/Home', methods=['GET', 'POST', 'OPTIONS'])
def publish_subscribe():
    global M
    global temp
    if request.method == 'GET':
        return {'time': 1}
    if request.method == 'POST':

        # information POST from netpage
        param_diction = request.get_json(force=True)
        if param_diction["type"]==1:
            print("start---------------------------------")
            message = {}
            message["message"]="hello"
            state={}
                

            state["reported"]={}
            state['reported']["time"] = str(datetime.datetime.now())
            state['reported']["threshold"] =float(param_diction["threshold"])
            state['reported']["ip"] =ip
            state['reported']["local_host"] =local_host
            state['reported']['lumin']=temp
            message["state"]=state
            messageJson=json.dumps(message)
            print(myAWSIoTMQTTClient.publish(topic,messageJson,1))
            print('Published topic %s: %s\n' % (topic, messageJson))
            print(param_diction["threshold"])
            return {"ifchange": datetime.datetime.now()}
        if param_diction["type"]==-1:
            print("start---------------------------------")
            message = {}
            message["message"]="hello"
            state={}
                

            state["reported"]={}
            state['reported']["time"] = str(datetime.datetime.now())
            state['reported']["opentime"] =str(param_diction["opentime"])
            state['reported']["ip"] =ip
            state['reported']["local_host"] =local_host
            state['reported']['lumin']=temp
            message["state"]=state
            messageJson=json.dumps(message)
            print(myAWSIoTMQTTClient.publish(topic,messageJson,1))
            print('Published topic %s: %s\n' % (topic, messageJson))
            print(param_diction["opentime"])
            return {"ifchange": datetime.datetime.now()}
        if param_diction["type"]==-2:
            print("start---------------------------------")
            message = {}
            message["message"]="hello"
            state={}
                

            state["reported"]={}
            state['reported']["time"] = str(datetime.datetime.now())
            state['reported']["closetime"] =str(param_diction["closetime"])
            state['reported']["ip"] =ip
            state['reported']["local_host"] =local_host
            state['reported']['lumin']=temp
            message["state"]=state
            messageJson=json.dumps(message)
            print(myAWSIoTMQTTClient.publish(topic,messageJson,1))
            print('Published topic %s: %s\n' % (topic, messageJson))
            print(param_diction["closetime"])
            return {"ifchange": datetime.datetime.now()}

        if param_diction["type"]==2:
            myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
             #time.sleep(0.5)
            print(M)
            temp=M["state"]["reported"]["lumin"]
            return {"ifchange":M["state"]["reported"]["lumin"]}
        if param_diction["type"]==3:
            myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
            #time.sleep(0.5)
            print("subscirbe part M ----------------------------")
            print(M)
            print("----------------------------")
            temp=M["state"]["reported"]["lumin"]
            return {"data":M["state"]["reported"]["lumin"]}
            
       
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9898, debug=True)
