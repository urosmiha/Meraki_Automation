from sqlite3 import Timestamp
from textwrap import indent
from turtle import delay
import paho.mqtt.client as mqtt
import time
import json
import requests
from requests.auth import HTTPBasicAuth

from env import MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PSW, CAMERA_SERIAL

PREVIOUS_TS = 1658312868371

def on_connect(client, userdata, flags, rc):
    '''
    connection notification that the script is running

    RC codes:
        0: Connection successful
        1: Connection refused – incorrect protocol version
        2: Connection refused – invalid client identifier
        3: Connection refused – server unavailable
        4: Connection refused – bad username or password
        5: Connection refused – not authorised
        6-255: Currently unused.
    '''

    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("/merakimv/{}/#".format(CAMERA_SERIAL))


def on_message(client, userdata, message):
    '''
    The callback for when a PUBLISH message is received from the mqtt server
    '''
    # For debug...
    # print("Received message '" + str(message.payload) + "' on topic '"
    #     + message.topic + "' with QoS " + str(message.qos))

    # Parse data from utf-8 to json so we can easily manipulate it
    payload = json.loads(message.payload.decode("utf-8", "ignore"))

    if "/merakimv/" in message.topic:
        notifyOnPeoplePresence(message, payload)
    # elif message.topic == 


def notifyOnPeoplePresence(message, payload):

    global PREVIOUS_TS

    # do some "magic" to display the number of people in the frame
    # The topic ending with "/0" is for the enrire frame - you can do this for idividual areas you highlighted as well
    # The 698057942242427412 is specific for a zone we added in the camera settings
    # This is used to see a total number of objects (e.g. people) in the frame
    if message.topic[-2:] == "12":
        # print(json.dumps(payload, indent=2))
        people = payload["counts"]["person"]
        # print("I see {} people".format(people))
        if people > 0:
            # Look at the time stamp and only notify every 1 minute to avoid spamming webex
            time_diff = ((payload['ts'] - PREVIOUS_TS) / 60 / 1000)
            if  time_diff > 1:
                PREVIOUS_TS = payload['ts']
                # print(json.dumps(payload, indent=2)) #debug..
                notifyMeWebex(payload['ts'])


def notifyMeWebex(timestamp):
    print("hello")


if __name__ == "__main__":

    print(MQTT_SERVER)
    try:
        # Create new MQTT client
        client = mqtt.Client()
        # Bind callback to callback function (on_connect())
        client.on_connect = on_connect
        # Bind message fucntion
        client.on_message = on_message
        client.username_pw_set(MQTT_USER, password=MQTT_PSW)
        # Connect to Broker.
        client.connect(MQTT_SERVER, MQTT_PORT, 60)

        client.loop_forever() 

    except Exception as ex:
        print("[MQTT]failed to connect or receive msg from mqtt, due to: \n {0}".format(ex))

