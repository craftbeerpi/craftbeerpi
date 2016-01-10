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
                                  (C) 2015 www.CraftBeerPI.com    |:: '    |
                                                                   ~~----~~
----------------------------------------------------------------------------

EOF

while true; do
    read -p "Would you like run apt-get update & apt-get upgrade? (y/n): " yn
    case $yn in
        [Yy]* ) apt-get -y update; apt-get -y upgrade; break;;
        [Nn]* ) break;;
        * ) echo "(Y/N)";;
    esac
done

while true; do
    read -p "Would you like to install wiringPI? This is required to control the GPIO (y/n): " yn
    case $yn in
        [Yy]* ) git clone git://git.drogon.net/wiringPi;
        cd wiringPi;
        ./build; cd ..;
        rm -rf wiringPi;
        break;;
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

cat << "EOF"

----------------------------------------------------------------------------

 ___         _        _ _      _   _            ___ _      _    _           _
|_ _|_ _  __| |_ __ _| | |__ _| |_(_)___ _ _   | __(_)_ _ (_)__| |_  ___ __| |
 | || ' \(_-<  _/ _` | | / _` |  _| / _ \ ' \  | _|| | ' \| (_-< ' \/ -_) _` |
|___|_||_/__/\__\__,_|_|_\__,_|\__|_\___/_||_| |_| |_|_||_|_/__/_||_\___\__,_|


Default URL: http://<IP-Address>:5000

Shell Commands to controll the Server:

- Start:  sudo /etc/init.d/craftbeerpiboot start
- Status: sudo /etc/init.d/craftbeerpiboot status
- Stop:   sudo /etc/init.d/craftbeerpiboot stop

Happy Brewing!

www.CraftBeerPI.com

----------------------------------------------------------------------------
EOF
