import config
import model
from brewapp import manager
from model import *
from util import *
from views import base
from brewapp import app, socketio
import time
from flask import request
import os
from werkzeug import secure_filename
from views import base
import sqlite3
from buzzer import nextStepBeep, timerBeep, resetBeep
from flask_restless.helpers import to_dict
import json

ALLOWED_EXTENSIONS = set(['sqlite'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/kbupload', methods=['POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return ('', 204)
            return ('', 404)
    except Exception as e:
        return str(e)

@base.route('/kb', methods=['GET'])
def getBrews():
    conn = None
    try:
        conn = sqlite3.connect(app.config['UPLOAD_FOLDER']+'/kb_daten.sqlite')
        c = conn.cursor()
        c.execute('SELECT ID, Sudname, BierWurdeGebraut FROM Sud')
        data = c.fetchall()
        result = []
        for row in data:
            result.append( {"id": row[0], "name": row[1], "brewed": row[2]})
        return json.dumps(result)
    except Exception as e:
        app.logger.error("Read Kleiner Brauhelfer Data failed: " + str(e))
        return ('',500)
    finally:
        if conn:
            conn.close()

@base.route('/kb/select/<id>', methods=['POST'])
def upload_file(id):
    data =request.get_json()
    conn = None
    try:
        ## Clear all steps
        Step.query.delete()
        db.session.commit()

        conn = sqlite3.connect(app.config['UPLOAD_FOLDER']+'/kb_daten.sqlite')
        c = conn.cursor()
        order = 0
        c.execute('SELECT EinmaischenTemp, Sudname FROM Sud WHERE ID = ?', (id,))
        row = c.fetchone()
        name = row[1]
        s = newStep("Einmaischen", order, "M", "I", row[0], 0, data['mashtun'])
        order +=1

    	### add rest step
        for row in c.execute('SELECT * FROM Rasten WHERE SudID = ?', (id,)):
            s = newStep(row[5], order, "A", "I", row[3], row[4], data['mashtun'])
            order +=1

        s = newStep("Laeuterruhe", order, "M", "I", 0, 15, 0)
        order +=1

		## Add cooking step
        c.execute('SELECT max(Zeit) FROM Hopfengaben WHERE SudID = ?', (id,))
        row = c.fetchone()
        s = newStep("Kochen", order, "A", "I", 100, row[0], data['boil'])
        order +=1

        ## Add Whirlpool step
        s = newStep("Whirlpool", order, "M", "I", 0, 15, data['boil'])
        order +=1

        setBrewName(name)

    except Exception as e:
        app.logger.error("Select Kleiner Brauhelfer Data failed: " + str(e))
        return ('',500)
    finally:
        if conn:
            conn.close()
    return ('',204)

## Helper method to create a new step
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
