#!/bin/bash
sleep 2
sudo killall python
cd /home/pi/drumkit
#./drumkit-rgb.py&
./drumkit-wristband.py 192.168.1.38&
