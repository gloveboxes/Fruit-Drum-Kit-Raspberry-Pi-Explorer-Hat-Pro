#!/bin/bash

sudo apt-get update
sudo apt-get dist-upgrade -y

sudo pip install paho-mqtt -q
sudo apt-get install xrdp -y
sudo apt-get install iceweasel -y

chmod +x *.sh
chmod +x *.py

sudo cp /home/pi/drumkit/drumkit.service /etc/systemd/system/
sudo systemctl enable drumkit.service

curl -sS get.pimoroni.com/explorerhat | bash