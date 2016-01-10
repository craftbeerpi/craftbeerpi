#!/bin/bash
#
# CraftBeer PI
#
# type the following commands:
# chmod +x install.sh
# sudo ./install.sh
# sudo reboot


clear
cat << "EOF"

----------------------------------------------------------------------------

   Weclome to
     _____            __ _   ____                 _____ _____ 	  _.._..,_,_
    / ____|          / _| | |  _  \              |  __  \_  _|   (          )
   | |     _ __ __ _| |_| |_| |_) | ___  ___ _ __| |__) /| |      ]~,"-.-~~[
   | |    | '__/ _` |  _| __|  _ < / _ \/ _ \ \'__|____/ | |    .=])' (;  ([
   | |____| | | (_| | | | |_| |_) |  __/  __/ |  | |    _| |_   | ]:: '    [
    \_____|_|  \__,_|_|  \__|____/ \___|\___|_|  |_|   |_____|  '=]): .)  ([
                                       (C) 2015 Manuel Fritsch    |:: '    |
                                                                   ~~----~~
----------------------------------------------------------------------------

EOF

while true; do
    read -p "Would you like run apt-get update & apt-get upgrade? (Y/N): " yn
    case $yn in
        [Yy]* ) apt-get -y update; apt-get -y upgrade; break;;
        [Nn]* ) break;;
        * ) echo "(Y/N)";;
    esac
done

#Install pip (package installer):
#apt-get -y install python-setuptools
easy_install pip

#Install PySerial
#pip install pyserial

#Install Python i2c and smbus
#apt-get -y install python-smbus

#Install Flask
apt-get -y install python-dev
apt-get -y install libpcre3-dev
pip install -r requirements.txt

while true; do
    read -p "Would you like to start CarftBeerPI after boot? (y/n): " yn
    case $yn in
        [Yy]* ) sed "s@#DIR#@${PWD}@g" craftbeerpiboot > /etc/init.d/craftbeerpiboot

    chmod 755 /etc/init.d/craftbeerpiboot;
		update-rc.d craftbeerpiboot defaults;
		break;;
        [Nn]* ) break;;
        * ) echo "Please select (y/n): ";;
    esac
done

while true; do
    read -p "Reboot the Raspberry PI now? (y/n): " yn
    case $yn in
        [Yy]* ) reboot; break;;
        [Nn]* ) break;;
        * ) echo "Please select (y/n): ";;
    esac
done
