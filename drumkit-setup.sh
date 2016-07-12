#!/bin/bash

sudo pip install paho-mqtt -q
curl -sS get.pimoroni.com/explorerhat | bash

sudo cp /home/pi/drumkit/drumkit.service /etc/systemd/system/
sudo systemctl enable drumkit.service

#sudo cp /home/pi/vivid/wpa_supplicant.conf /etc/wpa_supplicant/
