#!/bin/bash
#
# CraftBeer PI
#


cd /home/pi/craftbeerpi

git clone git://git.drogon.net/wiringPi;
cd wiringPi;
./build; cd ..;
rm -rf wiringPi;

#Install pip (package installer):
apt-get -y install python-setuptools;
easy_install pip;

#Install Flask
apt-get -y install python-dev;
apt-get -y install libpcre3-dev;
pip install -r requirements.txt

echo 'dtoverlay=w1-gpio,gpiopin=4,pullup=on' >> "/boot/config.txt"

sed "s@#DIR#@${PWD}@g" config/craftbeerpiboot > /etc/init.d/craftbeerpiboot

chmod 755 /etc/init.d/craftbeerpiboot;
update-rc.d craftbeerpiboot defaults;
