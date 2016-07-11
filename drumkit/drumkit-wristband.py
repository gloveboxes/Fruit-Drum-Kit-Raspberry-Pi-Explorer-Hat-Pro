#!/usr/bin/env python
print("""
This example turns your Explorer HAT into a drum kit!

Hit any touch pad to hear a drum sound.

Press CTRL+C to exit.
""")


import signal
import pygame
import explorerhat
# https://pypi.python.org/pypi/paho-mqtt
import paho.mqtt.client as mqtt
import json

light = [{'MsgId':0,'LightId':[1,2],'Red':0,'Green':0,'Blue':255},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':255,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':0,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':0,'Green':255,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':0,'Green':0,'Blue':255},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':255,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':255,'Green':0,'Blue':0},
         {'MsgId':0,'LightId':[1,2],'Red':0,'Green':255,'Blue':0}
]

     


client = mqtt.Client()

LEDS = [4, 17, 27, 5]

samples = [
    'sounds/hat.wav',
    'sounds/smash.wav',
    'sounds/rim.wav',
    'sounds/ting.wav',
    'sounds/hit.wav',
    'sounds/thud.wav',
    'sounds/clap.wav',
    'sounds/crash.wav',
]

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = []
for x in range(8):
    sounds.append(pygame.mixer.Sound(samples[x]))


def handle(ch, evt):
    if ch > 4:
        led = ch - 5
    else:
        led = ch - 1
    if evt == 'press':
        client.publish('msstore/vivid/light/1', json.dumps(light[ch-1]))
        explorerhat.light[1].fade(0, 100, 0.1)
        sounds[ch - 1].play(loops=0)
        name = samples[ch - 1].replace('/home/pi/vivid/sounds/','').replace('.wav','')
        print("{}!".format(name.capitalize()))
    else:
        explorerhat.light[led].off()

def on_connect(client, userdata, flags, rc):
    explorerhat.light[0].on()
    print("Connected with result code "+str(rc))

def on_disconnect(client, userdata, rc):
    explorerhat.light[0].off()
    if rc != 0:
        print("Unexpected disconnection.")
        client.reconnect()



client.connect("rpizero.local", 1883, 60)
client.on_connect = on_connect
client.on_disconnect = on_disconnect



explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

signal.pause()
