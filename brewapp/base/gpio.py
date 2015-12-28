from model import *
from brewapp import brewinit
gpio_state = {}

@brewinit()
def setup():
    print "SETUP GPIO"
    gpios = GpioConfig.query.all()
    for g in gpios:
        gpio_state[g.gpio] = {"name":g.name, "state":False}


def setState(gpio, new_state):
    try:

        int_gpio = int(gpio)
        if(new_state != "True" and new_state != "False"):
 		         return "Wrong command"

        bool_new_state = str2bool(new_state)
        old_state = gpio_state[int_gpio].get("state")
        gpio_state[int_gpio]['state'] =  bool_new_state

        if(old_state != bool_new_state):
            print "SWITCH GPIO ", gpio
        else:
            print "SAME STATE ", gpio

        return "OK"
    except:
        return "EXCEPTION"

def toggle(gpio):
    int_gpio = int(gpio)
    old_state = gpio_state[int_gpio].get("state")
    if(old_state == False):
        gpio_state[int_gpio]['state'] = True
    else:
        gpio_state[int_gpio]['state'] = False

def str2bool(value):
    return {"True": True, "true": True}.get(value, False)

#def job():
#    setup()

#app.brewapp_jobs.append(setup)
