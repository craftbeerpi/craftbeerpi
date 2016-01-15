from signals import *
from brewapp import app
from views import base
#@brewinit()
def initBuzzer():
    pass

@next_step.connect_via(app)
def nextStepBeep(sender, **extra):
    print sender
    print extra
    print "BEEP!"

@reset_step.connect_via(app)
def woooho(sender, **extra):
    print sender
    print extra
    print "WOOHOO!"
