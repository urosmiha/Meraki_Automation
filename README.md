# Meraki_Automation
Random Cisco Meraki Automation. Includes:
- __main.py__ : Random API functions, mostly around templates and org/network/device details
- __mv_customcv.py__ : uses MQTT broker to get notified when customCV detects an object
- __mv_sense.py__ : uses MQTT to get notified when people are present at a location
- __mt_mqtt.py__ : work in progress, but whould contain examples of MQTT integration for MTs

If you are using this make sure you also have a env.py file, which will contain all the sensitive info (e.g. API Keys, Serial number, org ids, etc). Note that this file is part of git ignore and should not be uploaded to git.

## Set up the Python Environment

I recommend you to create python virtual environment for cleaner workplace:

Create new environment:
```
  python3 -m venv env/
```
Open the environment:
```
  source env/bin/active
```

Install python modules needed for this project
```
  pip install -r requirements.txt
```

# Meraki Lab

API key and Always-on lab can be found here: https://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology

Otheriwse, just use your own Meraki Org and API key: https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API

# MQTT

For more information on MQTT refer to our documentation: https://developer.cisco.com/meraki/mv-sense/#!mqtt/what-is-mqtt 
We support MQTT on:
- [Meraki MRs](https://documentation.meraki.com/MR/Other_Topics/MR_MQTT_Data_Streaming)
- Meraki MVs with MV Sense
- [Meraki MTs](https://documentation.meraki.com/MT/MT_General_Articles/MT_MQTT_Setup_Guide)

![image](https://user-images.githubusercontent.com/31491578/180136043-94f5e226-ce45-44cd-bb46-cbe37d1cba16.png)

## MQTT Setup

I use macOS so most of the specific commands are all relevant to macOS (it's for my personal reference - I forget things), but should geneerally be all the same gist.

### You need a broker.. not a financial one, but MQTT broker.
Typically we you might want to use Raspberry Pi for this, or for a demo/prototype you can run this on your local PC (that's what I'm doing here).

I recommend using MQTT Mosquitto... you can download it from [here](https://mosquitto.org/)

In a terminal install mosquitto using [brew](https://brew.sh/)
```
brew install mosquitto
```

### Start Mosquitto
By default Mosquitto
- use __localhost__ and port __1883__
- No encryption and no username or password required

In terminal type
```
/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```
If you need to stop or restart mosquitto service
```
brew serivces stop mosquitto
```

### Config changes

We would need to make a few changes to the config file: __mosquitto.conf__. 

For MacOS, typically this is located in _/usr/local/etc/mosquitto/_ folder

Open Finder and press 'cmd' + ' Shift' + 'G' and seach the path

#### Add username and password
1. In the same folder create a file: e.g. __psw.txt__
2. Add username and password in the following format: __username:password__ e.g. rosi:psw123
3. Encrypt the password. In terminal type: 
```
mosquitto_passwd -c <path-to-your-password-file>
```
4. Open __mosquitto.conf__ and search and uncomment following settings:
 ```
 password_file <path-to-our-password-file>
 allow_anonymous false
 ```
This will ensure only validated connection can subscribe or publish to your broker.

#### Use your host's IP address for the broker
In order for Meraki MV, MS or MT to publish MQTT topics to your broker you need tell the broker to use your host's IP address.
1. Open __mosquitto.conf__, seach for and edit the following line:
 ```
 listener <port> <host-IP-address> 
 e.g. "listener 1883 10.10.10.4"
```

### Test
I would recommend to download [MQTT Explorer](http://mqtt-explorer.com/) to test connection to your MQTT broker.

Now that MQTT is running we can get MV, MT and/or MR to publish topics to this broker. Refer to links above for guides.

# Python Script to subscribe to MQTT messages
In order to read topics published by Meraki MV, MT or MR, you need to have a subscriber. You can use MQTT Explorer to read the messages, or to actually do something with these you can have a python script.

## MQTT with customCV
This is file named __mv_customcv.py__

Note: Make sure to create a file named __env.py__ and include the following parameters as strings: MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PSW, CAMERA_SERIAL. Example:
```
MQTT_SERVER = "10.10.10.4"
MQTT_PORT = 1883 #Please note: integer
MQTT_USER = "rosi"
MQTT_PSW = "psw123"
CAMERA_SERIAL = "XXX-XXX-XXX"
```
It will subscribe to __/merakimv/{CAMERA_SERIAL}/custom_analytics__ topic. This is to avoid noise in case other cameras are also publishing something to the same broker

For now, script just reads the messages and displays when something is detected. Will integrate with Webex later...

[How to configure customCV on Meraki Dashboard](https://documentation.meraki.com/MV/Video_Analytics/MV_Sense_Custom_Computer_Vision)

# MQTT with MV Sense
In this example we are using MV Sense to detect people and display this information with our python script.
