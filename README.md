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
testMode = False

### File name of sonder file
tempSensorId = '28-03146215acff'

### GPIO Number for Heating
heating_pin = 17

## GPIO Number Agitator
agitator_pin = 18

## interval in which the new temperatur is read
temp_db_interval = 5

## heating interval in seconds
pid_interval = 5

## PID tuning parameter
pipP=102

pidI=100

pidD=5


###################################################################
#### INTERNAL DO NOT CHANGE PARAMETERS BELOW
gpioMode = False
heatingState = False
agitatorState = False
pidState = False
```


### Start der Anwendung

In das carfbeerpi verzeichnis wechseln 

#### Starten
```
sudo nohub python runserver.py &
```
Jetzt läuft die Anwendung im Hintergrund.

#### Stoppen

```
sudo netstat -ntlp
```
Hier den Python Process suchen und wie folgt stoppen

```
sudo kill <Process_Id>
```

```

   _____            __ _   ____                 _____ _____ 	_.._..,_,_	
  / ____|          / _| | |  _ \               |  __ \_   _|   (          )	
 | |     _ __ __ _| |_| |_| |_) | ___  ___ _ __| |__) || |      ]~,"-.-~~[	
 | |    | '__/ _` |  _| __|  _ < / _ \/ _ \ '__|  ___/ | |    .=])' (;  ([			
 | |____| | | (_| | | | |_| |_) |  __/  __/ |  | |    _| |_   | ]:: '    [			
  \_____|_|  \__,_|_|  \__|____/ \___|\___|_|  |_|   |_____|  '=]): .)  ([		
                                                                |:: '    |
 ---------------------------------------- (C) 2015 Manuel F.     ~~----~~

SET GPIO AGITATOR
AGITATOR GPIO OK
SET GPIO HEATING
HEATING GPIO OK
START PID
 START TEMP JOB
START STEP JOB
 * Running on http://0.0.0.0:5000/
```

Die Anwedung ist jetzt über http://<server_id>:5000 im Browser aufrufbar.

## Bedienung

### Kleiner Brauhelfer Import
Der Import ist noch recht einfach gehalten. Klick oben rechts auf Admin dann auf "kleiner Brauhelfer" und wähle "Import" aus. Dann wähslt du die Datei "kb_daten.sqlite" aus. 

Windows:
USER_HOME/.kleiner-brauhelfer/kb_daten.sqlite

Mac:
USER_HOME/.kleiner-brauhelfer/kb_daten.sqlite

Nach dem Import findest du in der Admin Oberfläche auf "Kleiner Brauhelfer->Liste" eine Liste aller Importierten Sude.
Wenn du auf "Laden" klickst werden die Schritte im CraftBeerPI mit den gewählen Sud überschrieben.

Standardmäßig wird als erster Schritt ein "manueller Schritt" bei CraftBeerPI für die Einmaischtemperatur hinzugefügt. Anschließend kommen alle Rasten aus dem "kleinen Brauhelfer". Abschließend wird noch die längste Kochezeit des gewählten Sudes als "Koch-Schritt" mit hinzugefügt.

## Schritte Bearbeiten
Die Schritte können auf dem Tab "Schritte" in der Admin Oberfläche des CraftBeerPI bearbeitet werden.
Die Reihenfolge kann durch das Feld "order" definiert werden.

## Hardware Setup für den Testaufbau

* 1 x 1-wire Temperatursensor DS1820 Wasserdicht! (ebay)
* Tauchhülse Edelstahl - in gewünschter Länge (sensorshop24.de) 
* 1 x 4.7k Ohm Widerstand (Pollin.de, Conrad.de, Reichelt.de)
* Jumper Kabel (ebay) (Am besten gleich alle Varianten kaufen Stecker-Buchse, Buchse-Buchse, Stecker-Stecker So hat man Spielraum) 
* 2 x Solid-State Relais XURUI (Pollin.de, Conrad.de, Reichelt.de)
* Strangkühlkörper KAB-60 (Pollin.de, Conrad.de, Reichelt.de)
* Labor-Steckboard SYB-46 (Pollin.de, Conrad.de, Reichelt.de)
* Raspberry Pi (Model A+, 2 Model B) + Netzkabel + passende SDCard (Pollin.de, Conrad.de, Reichelt.de)
* 2 x Steckdose (Baumarkt)
* Schrauben zum befestingen der Bauteile (Baumarkt)


![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Hardwaresetup.png)
![ScreenShot](https://raw.githubusercontent.com/Manuel83/craftbeerpi/master/docs/images/Hardwaresetup2.png)