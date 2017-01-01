
import util
from model import *
from brewapp import app



def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "0000000000000000"

  return cpuserial

@util.brewinit(config_parameter="SEND_STATS")
def sendStats():
    app.logger.info("Sending stats")
    try:
        serial = getserial()
        info = {
        "id": serial,
        "version": "2.2",
        "kettle": [],
        "hardware": [],
        "thermometer": app.brewapp_thermometer.__class__.__name__,
        "hardware_control": app.brewapp_hardware.__class__.__name__
        }
        for k in Kettle.query.all():
            info["kettle"].append({"name": k.name, "diameter":k.diameter, "height": k.height, "agitator": k.agitator, "heater": k.heater})

        for h in Hardware.query.all():
            info["hardware"].append({"name": k.name, "type":h.type})
        import requests
        r = requests.post('http://www.craftbeerpi.com/stats.php', json=info)
        app.logger.info(r)
    except Exception as e:
        app.logger.error("Sending stats failed: " + str(e))
