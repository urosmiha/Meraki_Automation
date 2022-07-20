from textwrap import indent
from turtle import delay
import paho.mqtt.client as mqtt
import time
import json
import requests
from requests.auth import HTTPBasicAuth

from env import MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PSW, MT_MAC_ADDR, MT_BUTTON


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

    # Subscirbe just to door sensor
    client.subscribe("meraki/v1/mt/L_698057942242448112")


def on_message(client, userdata, message):
    '''
    The callback for when a PUBLISH message is received from the mqtt server
    '''
    # For debug...
    # print("Received message '" + str(message.payload) + "' on topic '"
    #     + message.topic + "' with QoS " + str(message.qos))

    print("Hello")

    # Parse data from utf-8 to json so we can easily manipulate it
    payload = json.loads(message.payload.decode("utf-8", "ignore"))
    print(json.dumps(payload, indent=2))
        
    time.sleep(1)


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

