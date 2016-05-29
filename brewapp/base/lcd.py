from util import *
import time

try:
    import RPi.GPIO as GPIO
    app.logger.info("SETUP GPIO Module Loaded")


    from datetime import datetime

# Zuordnung der GPIO Pins (ggf. anpassen)
    LCD_RS = 7
    LCD_E  = 8
    LCD_DATA4 = 25
    LCD_DATA5 = 24
    LCD_DATA6 = 23
    LCD_DATA7 = 18

    LCD_WIDTH = 20          # Zeichen je Zeile
    LCD_LINE_1 = 0x80       # Adresse der ersten Display Zeile
    LCD_LINE_2 = 0xC0       # Adresse der zweiten Display Zeile
    LCD_LINE_3 = 0x94
    LCD_LINE_4 = 0xD4
    LCD_CHR = GPIO.HIGH
    LCD_CMD = GPIO.LOW
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    FIRST = 0
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))
    pass

@brewinit(config_parameter="USE_LCD")
def init_lcd():
    print "INIT LCD"
     ###############################################################################
    #AO 20160206
    #print "init"
    app.logger.info("--> AO Method: --> INIT")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_DATA4, GPIO.OUT)
    GPIO.setup(LCD_DATA5, GPIO.OUT)
    GPIO.setup(LCD_DATA6, GPIO.OUT)
    GPIO.setup(LCD_DATA7, GPIO.OUT)
    display_init()

    #print "myinit"
    #lcd.lcd_send_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    #lcd.lcd_message("                ")
    #lcd.lcd_send_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    #lcd.lcd_message("                " )
    ###############################################################################

def lcd_send_byte(bits, mode):
        # Pins auf LOW setzen
        GPIO.output(LCD_RS, mode)
        GPIO.output(LCD_DATA4, GPIO.LOW)
        GPIO.output(LCD_DATA5, GPIO.LOW)
        GPIO.output(LCD_DATA6, GPIO.LOW)
        GPIO.output(LCD_DATA7, GPIO.LOW)
        if bits & 0x10 == 0x10:
          GPIO.output(LCD_DATA4, GPIO.HIGH)
        if bits & 0x20 == 0x20:
          GPIO.output(LCD_DATA5, GPIO.HIGH)
        if bits & 0x40 == 0x40:
          GPIO.output(LCD_DATA6, GPIO.HIGH)
        if bits & 0x80 == 0x80:
          GPIO.output(LCD_DATA7, GPIO.HIGH)
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, GPIO.HIGH)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, GPIO.LOW)
        time.sleep(E_DELAY)
        GPIO.output(LCD_DATA4, GPIO.LOW)
        GPIO.output(LCD_DATA5, GPIO.LOW)
        GPIO.output(LCD_DATA6, GPIO.LOW)
        GPIO.output(LCD_DATA7, GPIO.LOW)
        if bits&0x01==0x01:
          GPIO.output(LCD_DATA4, GPIO.HIGH)
        if bits&0x02==0x02:
          GPIO.output(LCD_DATA5, GPIO.HIGH)
        if bits&0x04==0x04:
          GPIO.output(LCD_DATA6, GPIO.HIGH)
        if bits&0x08==0x08:
          GPIO.output(LCD_DATA7, GPIO.HIGH)
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, GPIO.HIGH)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, GPIO.LOW)
        time.sleep(E_DELAY)

def display_init():
        lcd_send_byte(0x33, LCD_CMD)
        lcd_send_byte(0x32, LCD_CMD)
        lcd_send_byte(0x28, LCD_CMD)
        lcd_send_byte(0x0C, LCD_CMD)
        lcd_send_byte(0x06, LCD_CMD)
        lcd_send_byte(0x01, LCD_CMD)

def lcd_message(message):
        message = message.ljust(LCD_WIDTH," ")
        for i in range(LCD_WIDTH):
          lcd_send_byte(ord(message[i]),LCD_CHR)


###################################################################

@brewjob(key="lcdjob", interval=1,config_parameter="USE_LCD")
def lcdjob():
    global FIRST
    if (FIRST == 0):
        myinit()
    FIRST = FIRST + 1
    if (FIRST == 60):
        FIRST = 0

    ### DEIN LCD CODE HIER HIN!
    #------------------------------------------------------
    #TestAusgabe 2 (Uhrzeit
    #lcd_send_byte(LCD_LINE_1, LCD_CMD)
    #lcd_message(time.strftime("   %d.%m.%Y     "))
    #lcd_send_byte(LCD_LINE_2, LCD_CMD)
    #lcd_message(time.strftime("     %H:%M:%S     "))
    #------------------------------------------------------
    ## Skip if no step is active
    diff_sek = 0
    diff_min = 0
    diff_restSek = 0
    mynow = 0
    myend = 0
    #print "app.brewapp_kettle_state"
    #for x in app.brewapp_kettle_state:
    #    print (x)
    #    for y in app.brewapp_kettle_state[x]:
    #        print (y,':',app.brewapp_kettle_state[x][y])


    #ht1i = int(ht1.replace("GPIO", ""))
    #print "ht1: " + ht1.replace("GPIO", "") + " " + str(ht1i)
    #print "Heater1 " + str(GPIO.input(ht1i))

    try:
        ct = app.brewapp_kettle_state[1]["temp"]
        tt = app.brewapp_kettle_state[1]["target_temp"]
        ct2 = app.brewapp_kettle_state[2]["temp"]
        tt2 = app.brewapp_kettle_state[2]["target_temp"]

        ht1 = str(app.brewapp_kettle_state[1]["heater"])
        ht1x = GPIO.input(int(ht1.replace("GPIO", "")))
        ht2 = str(app.brewapp_kettle_state[2]["heater"])
        ht2x = GPIO.input(int(ht2.replace("GPIO", "")))

        ag1 = str(app.brewapp_kettle_state[1]["agitator"])
        ag1x = GPIO.input(int(ag1.replace("GPIO", "")))
        #print "ag1: " + ag1 + " ag1x: " + str(ag1x)[0:1]

    except:
        ct = 0
        ct2 = 0
        tt = 0
        tt2 = 0

    if(app.brewapp_current_step == None):
        cs = app.brewapp_current_step;

        lcd_send_byte(LCD_LINE_1, LCD_CMD)
        lcd_message("manuell         ")
        lcd_send_byte(LCD_LINE_2, LCD_CMD)
        lcd_message("T1: " + str(ct)[0:4] + "/" + str(format(tt, '01f'))[0:4] + "  H" + str(ht1x) + " A" + str(ag1x))
        lcd_send_byte(LCD_LINE_3, LCD_CMD)
        lcd_message("T2: " + str(ct2)[0:4] + "/" + str(format(tt2, '01f'))[0:4] + "  H" + str(ht2x))
    else:
        cs = app.brewapp_current_step;
        if(cs.get("timer_start") != None):
            myend = cs.get("endunix") + cs.get("timer")*60000
            mynow = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
            diff_sek = 0
            if (myend > mynow):
                diff_sek = (myend - mynow) / 1000
            else:
                diff_sek = 0
            diff_min = diff_sek / 60
            diff_restSek = diff_sek % 60
        lcd_send_byte(LCD_LINE_1, LCD_CMD)
        lcd_message(cs.get("name")[0:20])  #+ " " + str(diff_sek)
        lcd_send_byte(LCD_LINE_2, LCD_CMD)
        lcd_message("T1: " + str(ct)[0:4] + "/" + str(cs.get("temp"))[0:4] + "  H" + str(ht1x) + " A" + str(ag1x))
        lcd_send_byte(LCD_LINE_3, LCD_CMD)
        lcd_message("T2: " + str(ct2)[0:4] + "/" + str(format(tt2, '02f'))[0:4] + "  H" + str(ht2x) )
        lcd_send_byte(LCD_LINE_4, LCD_CMD)
        lcd_message("LZ: " + str(format(diff_min, '02d')) + ":" + str(format(diff_restSek, '02d')))
