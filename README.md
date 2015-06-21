# CraftBeer PI


## Installation

### Raspbian installieren (Noobs)

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