from signals import *
from brewapp import app
from views import base
from util import *

#@brewinit()
def initBuzzer():
    pass

@next_step.connect_via(app)
def nextStepBeep(sender, **extra):
    print "NEXT"

@start_timer.connect_via(app)
def timer(sender, **extra):
    print "TIMER"

@reset_step.connect_via(app)
def reset(sender, **extra):
    print "REST"
