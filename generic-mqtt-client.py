#!/usr/bin/python2.7
import sys
import time
import os
import string
import random
import dbus
import paho.mqtt.client as mqtt
import json                     # for reading the configuration

print "Starting"

config_file = sys.argv[1] if len(sys.argv) > 1 else None
if config_file == None:
    config_file = os.environ["HOME"] + "/.config/generic-mqtt-client.conf"

with open(config_file) as json_file:
    config = json.load(json_file)

mqtt_client_id = str(config["client_id"])
mqtt_server    = str(config["server"])
mqtt_port      = config["port"]
mqtt_keepalive = config["keepalive"]
mqtt_topic     = str(config["topic"])
mqtt_qos       = config["qos"]
notify_app     = config["notify-app"]

print "starting MQTT notification client!"
print "Press CTRL + C to exit"

def on_log(mosq, obj, level, string):
    print(string)

def on_connect(mosq, userdata, rc):
    if rc == 0:
        print("Connected to: "+mqtt_server+" topic "+mqtt_topic)
        mqttc.subscribe(mqtt_topic, mqtt_qos)
    else:
        print("Connection failed with error code: "+str(rc))

# Note: In case you are connecting to an older version of Mosquitto, you'll need to set this to mqtt.MQTTv31!
mqttc = mqtt.Client(mqtt_client_id, False, None, mqtt.MQTTv311 )

if "credentials" in config:
    mqttc.username_pw_set(config["credentials"]["user"], config["credentials"]["password"])
mqttc.on_log = on_log
mqttc.on_connect = on_connect
# Setting reconnect delay is currently not supported by paho
#mqttc.reconnect_delay_set(1, 300, True)
mqttc.connect(mqtt_server, mqtt_port, mqtt_keepalive)

def on_message(mosq, obj, msg):
    print("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)
    notification = msg.payload.split('\n')
    try:
        interface.Notify(notify_app,
                 0,
                 "icon-m-notifications",
                 notification[0],
                 notification[1],
                 dbus.Array(["default", ""]),
                 dbus.Dictionary({"category":"x-nemo.messaging.mqtt",
                             "x-nemo-preview-body": notification[1],
                             "x-nemo-preview-summary": notification[0]},
                             signature='sv'),
                 0)
    except dbus.exceptions.DBusException:
        print("Failed sending DBus notification.")

mqttc.on_message = on_message

bus = dbus.SessionBus()
object = bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
interface = dbus.Interface(object,'org.freedesktop.Notifications')

mqttc.loop_forever()
