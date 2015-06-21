# CraftBeer PIv0.1

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

### Python Pakete Installieren

Ins CraftBeerPI Verzeichnis wechseln und folgenden Befehlt ausführen
```
sudo pip install -r requirements.txt
```
### Konfiguration


## Hardware Setup

![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Hardwaresetup.png)
