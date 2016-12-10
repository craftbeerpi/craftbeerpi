# CraftBeerPI v2.1
The Raspberry PI base Home Brewing Software

Website: www.CraftBeerPI.com

## Features

* Simple and easy installation script
* Flexible Kettle Setup - From simple 1 kettle preserving cooker to 3 kettle RIMS or HERMS setup
* Flexible Brew Step Configuraiton - Configure your own brew steps. From mashing over boiling to whirlpool
* Automatic Timer Control. The Step Control will take care of your brew steps.
* Import Recipes from "Kleiner Brauhelfer" -Plan your brew at "Kleiner Brauhelfer" and import the recipes to CraftBeerPI
* Heater & Agitator Control - Control heater and agitator via web interface
* Temperature Chart - Temperature data is recorded and display as a line chart
* Mobile Device UI - Control your brew form Smartphone or Tablet
* Additional Hardware like pumps or vents can be controlled
* Brew Automatic with Overshoot Logic, PID Logic, Fermentation Logic.
* Custom Automatic logics can be add
* Recipe Book
* Support für GPIO, PiFace or Gembird USB Socket
* Temperature can be measured in Fahrenheit or Celcius

## Support & Communities

The Community of CraftBeerPi is quite active.

Facebook:

http://facebook.com/craftbeerpi

German Forum:

http://hobbybrauer.de/forum/viewtopic.php?f=58&t=3959

Australian Forum:

http://aussiehomebrewer.com/topic/90757-craftbeerpi-brew-controller/

US Forum:

http://www.homebrewtalk.com/showthread.php?t=569497

Canadian Forum:

https://www.canadianhomebrewers.com/viewtopic.php?f=12&t=4011&sid=d58dfec3f5959858f4ed7f2f3d3404d7

Norwegian Forum

https://forum.norbrygg.no/threads/craftbeerpi-styrings-software-for-raspberry-pi.33478/

Brazilian Forum
http://www.homebrewtalk.com.br/showthread.php?t=408096

## Screenshots

![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Screenshot1.png)
![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Screenshot2.png)


## Installation



### Raspbian (Noobs)

Here you will find the guide to install Raspbian

https://www.raspberrypi.org/help/noobs-setup/

Please select Raspbina as operating system.


### CraftBeer PI Installation

Watch the installation video or read the installation steps below

[![asciicast](https://asciinema.org/a/du84msz9t56yqqg6j6qfjmvjd.png)](https://asciinema.org/a/du84msz9t56yqqg6j6qfjmvjd)

Clone CraftBeerPI from GitHub.
Open the shell on your Raspberry PI and type the following command.
```
git clone https://github.com/Manuel83/craftbeerpi.git
```
### Setup Script

After cloning the program to your Raspberry PI you just have to run the install.sh script.
The script will guide you through the installation process.
```
sudo ./install.sh
```

### Automatic start after boot

As part of the installation you will ask if you like to start CraftBeerPI after boot automatically.
If you have selected this at the first installation just run the installation again and
select 'y' when you are ask if CraftBeerPI should start after boot.

#### Start the Server manually
```
sudo python runserver.py
```

The App is now available under:  http://<server_id>:5000

## Manual

### Kleiner Brauhelfer Import
To import the database from "Kleiner Brauhelfer" select "Steps".
There you will find a button "Import Kleiner Brauhelfer". Upload the kb_daten.sqlite of
Kleiner Brauhelfer.

You will find the sqlite file on your computer at.

Windows:
USER_HOME/.kleiner-brauhelfer/kb_daten.sqlite

Mac:
USER_HOME/.kleiner-brauhelfer/kb_daten.sqlite

Refresh the "Import Kleiner Brauhelfer" page. Select the brew you want to load.
After this you will asked for the MashTun and the Boil kettle of the brew.

## Hardware Setup

* 1 x 1-wire Temperatursensor DS1820 Waterproof! (ebay)
* Thermowell stainless steel - in gewünschter Länge (sensorshop24.de)
* 1 x 4.7k Ohm Resistor (Pollin.de, Conrad.de, Reichelt.de)
* Jumper Cable (ebay)
* 2 x Solid-State Relais XURUI (Pollin.de, Conrad.de, Reichelt.de)
* Heatsink KAB-60 (Pollin.de, Conrad.de, Reichelt.de)
* Breadboard SYB-46 (Pollin.de, Conrad.de, Reichelt.de)
* Raspberry Pi (Model A+, 2 Model B) + Power Cable + SDCard (Pollin.de, Conrad.de, Reichelt.de)


![ScreenShot](http://craftbeerpi.com/img/Img1.png)

## Start CraftBeerPI in Kiosk Mode

The Kiosk Mode requires that CraftBeerPI is start at boot.
Make sure that SSH is still enabled otherwise its not possible remove this kiosk mode.


```
sudo raspi-config
```

Change your boot to desktop environment. This will start-up the GUI instead of the CLI and automatically will login to user 'pi'.

Install Chromium Browser
```
sudo apt-get install chromium
```

Change startup Config

```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

Change the file that it looks like this

```
@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xset s off
@xset -dpms
@xset s noblank
@sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences
@chromium --noerrdialogs --kiosk http://localhost:5000 --incognito
```

Reboot the Raspberry PI

```
sudo reboot
```

### Implementing a custom thermometer protocol
Out of the box CraftBeerPI is supporting 1-wire thermometers.
But integrating a custom thermometer protocol is quite simple.

Just overwrite 3 simple method of the w1_thermometer.py

```
## This method gets invoked only once during start time.
## This is the right place if the Thermometer needs to be initialize
## during server start.
@brewinit()
def initThermo():
    #Custom Code here
    # no return value

## Define which Thermometers are available
## Return the id/name of available thermometers as string array
def getW1Thermometer():
    ## Custom code here!
    return ["DummySensor1","DummySensor2"]

## This method gets invoked every 5 seconds for each thermometer
## Just read the current value and return it a float
def tempData1Wire(tempSensorId):
    ## Custom code here!
    return 100.00
```
