# CraftBeerPI v0.1
                                                         
## Features

* Temperaturverlaufsanzeige (Real-Time)
* Frei Konfigurierbarer Ablaufplan mit manuellen und automatischen Schritten
* Timer mit automatischem Start bei erreichen der Zieltemperatur
* Digitales Brauprotokoll
* Smartphone und Tablet optimiert 
* WebSocket Push Notification für Real-Time Update
* Admin Oberfläche
* WLAN Zugriff
* Automatische Heizsteuerung (PID Controller)
* Sud Import aus dem "kleinen Brauhelfer"

## Screenshots

![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Screenshot1.png)
![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Screenshot2.png)


## Installation

### Raspbian installieren (Noobs)

Hier findet ihr eine Anleitung zur Installation von Noobs.

https://www.raspberrypi.org/help/noobs-setup/

Bitte als Betriebsystem Raspbian auswählen.

### WIFI Auf dem Raspberry PI konfigurieren

Nach WLAN scannen
```
sudo iwlist wlan0 scan
```
WLAN Config Datei öffnen
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Netzwerk und Passwort eingeben
```
network={
    ssid="The_ESSID_from_earlier"
    psk="Your_wifi_password"
}
```
WLAN Adapter stoppen
```
sudo ifdown wlan0
```
WLAN Adapter starten
```
sudo ifup wlan
```
### WiringPi installieren
```
sudo apt-get update
sudo apt-get upgrade
git clone git://git.drogon.net/wiringPi
cd wiringPi
git pull origin
cd wiringPi
./build
```
### Pip für Python 2.7 installieren
```
sudo apt-get install python-pip
```
### CraftBeer PI herunterladen
Am einfachsten ist wenn man die Software in das Home Verzeichnis des Benutzers pi wie folgt kopiert
```
git clone https://github.com/Manuel83/craftbeerpi.git
```
### Python Pakete Installieren

Ins CraftBeerPI Verzeichnis wechseln und folgenden Befehlt ausführen
```
sudo pip install -r requirements.txt
```
### Konfiguration

Die Konfiguraitonsdatei ist in folgenen Verzeichnis zu finden

craftbeerpi/brewapp/globalprops.py

```
nano globalprops.py
```


Konfiguraitonsdatei

```
## if test mode
testMode = True

### File name of sonder file
tempSensorId = '28-03146215acff'

### GPIO Number for Heating
heating_pin = 17

## GPIO Number Agitator
agitator_pin = 18

## interval in which the new temperatur is read
temp_db_interval = 5

## heating interval in seconds
pid_interval = 10

## PATH WHERE THE kleiner Brauhelfer DB is stored after upload
kb_path = '/Users/manuelfritsch/Documents/git/python'

###################################################################
#### INTERNAL DO NOT CHANGE PARAMETERS BELOW
gpioMode = False
heatingState = False
agitatorState = False
pidState = False
```


### Start der Anwendung

In das carfbeerpi verzeichnis wechseln 
```
sudo python runserver.py
```


## Hardware Setup

![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Hardwaresetup.png)
