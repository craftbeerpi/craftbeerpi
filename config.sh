#!/bin/bash

clear;
cat << "EOF"

The installation must be set to auto start for using this tool!!

1 = start CraftBeerPi
2 = stop CraftBeerPi
3 = status of CraftBeerPi
4 = Add this installation to auto start
5 = Remove this CraftBeerPi installation from auto start

EOF

while true; do
    read -p "Please select a number: " yn
    case $yn in
        [1]* ) sudo /etc/init.d/craftbeerpiboot start break;;
        [2]* ) sudo /etc/init.d/craftbeerpiboot stop break;;
        [3]* ) sudo /etc/init.d/craftbeerpiboot status break;;
        [4]* ) sed "s@#DIR#@${PWD}@g" config/craftbeerpiboot > /etc/init.d/craftbeerpiboot
        chmod 755 /etc/init.d/craftbeerpiboot
		update-rc.d craftbeerpiboot defaults
		break;;
        [5]* ) update-rc.d craftbeerpiboot remove; break;;
        * ) break;;
    esac
done
