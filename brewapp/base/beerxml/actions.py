import xml.etree.ElementTree

from brewapp.base.model import *
from werkzeug import secure_filename
from brewapp.base.util import *
from brewapp.base.views import base
from brewapp import app, socketio
from flask import request

import json
print "HALLO"
ALLOWED_EXTENSIONS = set(['xml'])
BEER_XML_FILE = "./upload/recipes.xml"

def getRecipeName(id):
    e = xml.etree.ElementTree.parse(BEER_XML_FILE).getroot()
    return e.find('./RECIPE[%s]/NAME' % (str(id))).text

def getBoilTime(id):
    e = xml.etree.ElementTree.parse(BEER_XML_FILE).getroot()
    return e.find('./RECIPE[%s]/BOIL_TIME' % (str(id))).text


def getSteps(id):
    e = xml.etree.ElementTree.parse(BEER_XML_FILE).getroot()
    steps = []
    for e in e.findall('./RECIPE[%s]/MASH/MASH_STEPS/MASH_STEP' % (str(id))):
        if app.brewapp_config.get("UNIT", "C") == "F":
            step_temp = format(9.0/5.0 * float(e.find("STEP_TEMP").text) + 32, 'f')
        else:
            step_temp = e.find("STEP_TEMP").text
        steps.append({"name": e.find("NAME").text, "temp": step_temp, "timer": e.find("STEP_TIME").text})

    return steps

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def newStep(name, order, type, state, temp = 0, timer = 0, kettileid = 0):
    s = Step(name=name, order=order, type=type, state=state, temp=temp, timer=timer, kettleid=kettileid)
    db.session.add(s)
    db.session.commit()
    return s

def setBrewName(name):
    config = Config.query.get("BREWNAME");

    if(config == None):
        config = Config()
        config.name = "BREWNAME"
        config.value = name

    else:
        config.value = name

    db.session.add(config)
    db.session.commit()

@app.route('/api/beerxml/upload', methods=['POST'])
def uploadBeerXML():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "recipes.xml"))
                return ('', 204)
            return ('', 404)
    except Exception as e:
        return str(e)

@app.route('/api/beerxml', methods=['GET'])
def getAllFromBeerXML():
    e = xml.etree.ElementTree.parse(BEER_XML_FILE).getroot()
    result = []
    for idx, val in enumerate(e.findall('RECIPE')):
        result.append({"id": idx, "name": val.find("NAME").text})
    return json.dumps(result)


@app.route('/api/beerxml/select/<id>', methods=['POST'])
def selectFromBeerXML(id):
    try:
        data = request.get_json()
        ## Clear all steps
        Step.query.delete()
        db.session.commit()
        order = 0
        stesps = getSteps(int(id))
        print stesps
        for s in getSteps(int(id)):
            temp = float(format(float(s.get("temp", 0.00)), '.2f'))
            s = newStep("MashIn", order, 'M' if order == 0 else 'A', "I", temp, s.get("timer", 0), data['mashtun'])
            order += 1

        s = newStep("Chilling", order, "M", "I", 0, 15, 0)
        order +=1
        if app.brewapp_config.get("UNIT", "C") == "F":
            boil_temp = 210
        else:
            boil_temp = 99
        s = newStep("Boil", order, "A", "I", boil_temp, getBoilTime(int(id)), data['boil'])
        order +=1

        ## Add Whirlpool step
        s = newStep("Whirlpool", order, "M", "I", 0, 15, data['boil'])
        order +=1

        setBrewName(getRecipeName(int(id)))

    except Exception as e:
        app.logger.error("Select BeerXML Data failed: " + str(e))
        print e
        return ('',500)

    return ('',204)

