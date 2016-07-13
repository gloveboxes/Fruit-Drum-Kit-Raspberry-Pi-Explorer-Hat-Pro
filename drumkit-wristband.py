#!/usr/bin/env python
print("""
This example turns your Explorer HAT into a drum kit!

Hit any touch pad to hear a drum sound.

Press CTRL+C to exit.
""")


import signal
import pygame
import explorerhat
import json
import base64

# https://pypi.python.org/pypi/paho-mqtt
# http://www.eclipse.org/paho/clients/python/docs/

import paho.mqtt.client as mqtt


light = [{'MsgId':0,'LightId':[1,2],'Red':0,'Green':0,'Blue':255},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':255,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':0,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':0,'Green':255,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':0,'Green':0,'Blue':255},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':255,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':0,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':0,'Green':255,'Blue':0}
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
    'sounds/drums/hit.wav',
    'sounds/drums/thud.wav',
    'sounds/drums/clap.wav',
    'sounds/drums/crash.wav',
    'sounds/balmer/iltc_I.wav',
    'sounds/balmer/iltc_love.wav',
    'sounds/balmer/iltc_this.wav',
    'sounds/balmer/iltc_company.wav',
    'sounds/beep.wav',
]


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = []
for x in range(9):
    sounds.append(pygame.mixer.Sound(samples[x]))


def handle(ch, evt):
    global drumMode
    if evt == 'press':
        if ch == 1 or ch == 2:
            print(str(ch))
            explorerhat.light.blue.off()
            explorerhat.light.yellow.off()        
            drumMode = ch - 1            
            sounds[8].play(loops=0)
            explorerhat.light[drumMode].on()
            return
        if ch == 3 or ch == 4:
            return
        
        client.publish('dmx/data', json.dumps(light[ch-1]))
        explorerhat.light.red.fade(0, 100, 0.1)
        instrument = ((ch - 5) + (drumMode * 4))
        #print("Instrument " + str(instrument))
        
        sounds[instrument].play(loops=0)
        name = samples[instrument].replace('sounds/','').replace('.wav','')
        print("{}!".format(name.capitalize()))
    else:
        explorerhat.light.red.off()

def on_connect(client, userdata, rc):
    explorerhat.light.green.on()
    print("MQTT Connected with result code "+str(rc))

def on_disconnect(client, userdata, rc):
    explorerhat.light.green.off()
    print("MQTT Disconnected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async("rpizero.local", 1883, 60)
client.loop_start()

explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

signal.pause()
