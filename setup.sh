#!/bin/bash

sudo apt-get update
sudo apt-get dist-upgrade -y
sudo pip install paho-mqtt -y
sudo apt-get install xrdp -y
sudo apt-get install iceweasel -y
curl -sS get.pimoroni.com/explorerhat | bash

sudo cp /home/pi/drumkit/drumkit.service /etc/systemd/system/
sudo systemctl enable drumkit.service

sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.old
sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
sudo cp wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

#sudo cp /home/pi/vivid/wpa_supplicant.conf /etc/wpa_supplicant/
