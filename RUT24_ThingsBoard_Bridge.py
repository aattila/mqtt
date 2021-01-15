#!/usr/bin/env python3

'''
This script interrogates the RUT240 router attributes by using their MQTT broker (so please enable it)
and replicates the attributes to the ThingsBoard MQTT topic.

It is very useful when your RUT240 is behind of the NAT (and it will be, remember this is an LTE router)
and you want to monitorize - with an elegant dashboard - your router attributes.
'''

import paho.mqtt.client as mqtt
import json
import sys
import time

MQTT_TOKEN  = "<copy here the device token>"
MQTT_HOST = "<your thingsboard server host>"
MQTT_PORT = 1883

RUT_TYPE = "router"
RUT_HOST = "192.168.1.1"
RUT_PORT = 1883
RUT_SERIAL = ""
RUT_T_ID   = RUT_TYPE + "/id"
RUT_T_GET  = RUT_TYPE + "/get"

RUT_T_TEMP = ""
RUT_T_OPER = ""
RUT_T_SIGN = ""
RUT_T_NETW = ""
RUT_T_CONN = ""
RUT_T_WAN = ""
RUT_T_UPT = ""
RUT_T_NAME = ""
RUT_T_PIN3 = ""
RUT_T_PIN4 = ""

rut_data = {'temperature': 0.0, 'operator': '', 'signal': 0, 'network': '', 'connection': '', 'wan': '', 'uptime': '', 'name': '', 'pin3': 0, 'pin4': 0}

def uptime(total_seconds):

     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24

     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )

     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

     return string;

def on_message(client, userdata, message):
    global RUT_SERIAL
    global RUT_T_TEMP
    global RUT_T_OPER
    global RUT_T_SIGN
    global RUT_T_NETW
    global RUT_T_CONN
    global RUT_T_WAN
    global RUT_T_UPT
    global RUT_T_NAME
    global RUT_T_PIN3
    global RUT_T_PIN4

    '''
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    '''
    val = message.payload.decode("utf-8")
    if message.topic == RUT_T_ID:
        RUT_SERIAL = str(val)
        RUT_T_TEMP = RUT_TYPE + "/" + RUT_SERIAL + "/temperature"
        RUT_T_OPER = RUT_TYPE + "/" + RUT_SERIAL + "/operator"
        RUT_T_SIGN = RUT_TYPE + "/" + RUT_SERIAL + "/signal"
        RUT_T_NETW = RUT_TYPE + "/" + RUT_SERIAL + "/network"
        RUT_T_CONN = RUT_TYPE + "/" + RUT_SERIAL + "/connection"
        RUT_T_WAN  = RUT_TYPE + "/" + RUT_SERIAL + "/wan"
        RUT_T_UPT  = RUT_TYPE + "/" + RUT_SERIAL + "/uptime"
        RUT_T_NAME = RUT_TYPE + "/" + RUT_SERIAL + "/name"
        RUT_T_PIN3 = RUT_TYPE + "/" + RUT_SERIAL + "/pin3"
        RUT_T_PIN4 = RUT_TYPE + "/" + RUT_SERIAL + "/pin4"

    if message.topic == RUT_T_TEMP:
        rut_data["temperature"] = int(val)/10
    if message.topic == RUT_T_OPER:
        rut_data["operator"] = str(val)
    if message.topic == RUT_T_SIGN:
        rut_data["signal"] = val
    if message.topic == RUT_T_NETW:
        rut_data["network"] = str(val)
    if message.topic == RUT_T_CONN:
        rut_data["connection"] = str(val)
    if message.topic == RUT_T_WAN:
        rut_data["wan"] = str(val)
    if message.topic == RUT_T_UPT:
        rut_data["uptime"] = uptime(int(val))
    if message.topic == RUT_T_NAME:
        rut_data["name"] = str(val)
    if message.topic == RUT_T_PIN3:
        rut_data["pin3"] = int(val)
    if message.topic == RUT_T_PIN4:
        rut_data["pin4"] = int(val)


client = mqtt.Client(client_id="RUT240")
client.on_message=on_message
client.connect(RUT_HOST, RUT_PORT, 60)
client.loop_start()

# get the serial id
client.subscribe(RUT_T_ID)
client.publish(RUT_T_GET, "id")
time.sleep(3)

# subscribe to parameter topics
client.subscribe(RUT_T_TEMP)
client.subscribe(RUT_T_OPER)
client.subscribe(RUT_T_SIGN)
client.subscribe(RUT_T_NETW)
client.subscribe(RUT_T_CONN)
client.subscribe(RUT_T_WAN)
client.subscribe(RUT_T_UPT)
client.subscribe(RUT_T_NAME)
client.subscribe(RUT_T_PIN3)
client.subscribe(RUT_T_PIN4)

# request the parameter values
client.publish(RUT_T_GET, "temperature")
client.publish(RUT_T_GET, "operator")
client.publish(RUT_T_GET, "signal")
client.publish(RUT_T_GET, "network")
client.publish(RUT_T_GET, "connection")
client.publish(RUT_T_GET, "wan")
client.publish(RUT_T_GET, "uptime")
client.publish(RUT_T_GET, "name")
client.publish(RUT_T_GET, "pin3")
client.publish(RUT_T_GET, "pin4")
time.sleep(3)

#print(rut_data)


tboard = mqtt.Client()
tboard.username_pw_set(MQTT_TOKEN)
tboard.connect(MQTT_HOST, MQTT_PORT, 60)
tboard.loop_start()
tboard.publish('v1/devices/me/telemetry', json.dumps(rut_data), 1)

time.sleep(10)

tboard.loop_stop()
tboard.disconnect()
client.loop_stop()
client.disconnect()
