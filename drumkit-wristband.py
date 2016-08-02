#!/usr/bin/env python
print("""
This example turns your Explorer HAT into a drum kit!

Hit any touch pad to hear a drum sound.

Press CTRL+C to exit.
""")

import sys
import time
import signal
import pygame
import explorerhat
import json
import base64
import paho.mqtt.client as mqtt     # https://pypi.python.org/pypi/paho-mqtt and http://www.eclipse.org/paho/clients/python/docs/


mqttBroker = "rpidmx01.local"

wristbandColours = [16, 48, 160, 144, 0]

light = [
    {'id':[2,3,4,5,6,7,8,9],'Red':255,'Green':0,'Blue':0},     #red
    {'id':[2,3,4,5,6,7,8,9],'Red':0,'Green':255,'Blue':255},   #teal
    {'id':[2,3,4,5,6,7,8,9],'Red':255,'Green':255,'Blue':0},     #blue
    {'id':[2,3,4,5,6,7,8,9],'Red':255,'Green':0,'Blue':255},   #purple
    {'id':[2,3,4,5,6,7,8,9],'Red':0,'Green':0,'Blue':0},       #black all lights off
]

dmxMsg = {'id':[1],'data':'data'}

LEDS = [4, 17, 27, 5]
drumMode = 0;
explorerhat.light.blue.on()


samples = [
    #'sounds/drums/hat.wav',
    #'sounds/drums/smash.wav',
    #'sounds/drums/rim.wav',
    #'sounds/drums/ting.wav',
    'sounds/ben/kick.wav',
    'sounds/ben/snare.wav',
    'sounds/ben/hat.wav',
    'sounds/drums/hit.wav',
    'sounds/drums/thud.wav',
    'sounds/drums/clap.wav',
    'sounds/drums/crash.wav',
    'sounds/balmer/kick.wav',
   # 'sounds/balmer/snare.wav',
   # 'sounds/balmer/iltc_this.wav',
   # 'sounds/balmer/iltc_company.wav',
    'sounds/beep.wav',
]


#pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.pre_init(32000, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = []
for x in range(9):
    sounds.append(pygame.mixer.Sound(samples[x]))


def wristbandToJson(colour, channel):
    if channel < 1 or channel > 9:
        return
    if colour < 0 or colour > 4:
        return
    
    channel = channel - 1
    hexs = "00 00 00 00 00 00 00 00 00"
    data = bytearray.fromhex(hexs)
    data[channel] = wristbandColours[colour]
    channelData = base64.b64encode(data)
    jsonData ={'id':[1],'data':'' + channelData + ''}
    return json.dumps(jsonData)

def handle(ch, evt):
    global drumMode
    
    if evt == 'press':
        if ch == 1 or ch == 2:  # mode swap between drums and ballmer

            explorerhat.light.blue.off()
            explorerhat.light.yellow.off()
            explorerhat.light.red.off()
            
            drumMode = ch - 1                   #set drum mode: 0 = drums, 1 = ballmer
            sounds[8].play(loops=0)             #play status change sound
            explorerhat.light[drumMode].on()    #set status led
            
            return
        
        if ch == 3:             #set all wristbands and rgb lights to black/off
            
            explorerhat.light.red.on()  #set all black/off status light
            sounds[8].play(loops=0)     #play status change sound

            client.publish('dmx/data', wristbandToJson(4, 1))   # publish control data for wristband
            client.publish('dmx/data', json.dumps(light[4]))    # publish control data for rgb lights
            
            return

        if ch == 4:
            return

        explorerhat.light.red.off()     #resets all black/off status light

        client.publish('dmx/data', wristbandToJson(ch - 5, 1))  # publish control data for wristband
        client.publish('dmx/data', json.dumps(light[ch - 5]))   # publish control data for rgb lights

        instrument = ((ch - 5) + (drumMode * 4))    #Capacitive pads channels 5 to 8 - map to zero for sounds collection
        sounds[instrument].play(loops=0)


def on_connect(client, userdata, rc):
    explorerhat.light.green.on()        #Set MQTT Connected status led
    print("MQTT Connected with result code "+str(rc))
    

def on_disconnect(client, userdata, rc):
    explorerhat.light.green.off()       #set MQTT Disconnected status led
    print("MQTT Disconnected with result code "+str(rc))
    


if len(sys.argv) > 1:
    mqttBroker = sys.argv[1]
    print("MQTT Broker " + mqttBroker)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async(mqttBroker, 1883, 60)
client.loop_start()

explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

signal.pause()
