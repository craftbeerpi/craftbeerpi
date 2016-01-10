import config
import model
from brewapp import manager
from util import brewinit
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

from flask.ext.restless.helpers import to_dict

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

@app.route('/api/step/clear', methods=['POST'])
def getBrews():
    Step.query.delete()
    db.session.commit()
    return ('',204)

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
    except:
        return ('',500)
    finally:
        if conn:
            conn.close()


@base.route('/kb/select/<id>', methods=['POST'])
def upload_file(id):


    data  =request.get_json()
    print "Data", data
    conn = None
    try:
        Step.query.delete()
        db.session.commit()
        conn = sqlite3.connect(app.config['UPLOAD_FOLDER']+'/kb_daten.sqlite')
        c = conn.cursor()
        order = 0

        c.execute('SELECT EinmaischenTemp, Sudname FROM Sud WHERE ID = ?', (id,))
        row = c.fetchone()
        s = Step()
        s.name = "Einmaischen"
        s.order = order
        s.type = 'M'
        s.state = 'I'
        s.temp = row[0]
        s.timer = 0
        s.kettleid = data['mashtun']
        db.session.add(s)
        db.session.commit()
        order +=1

    	### add rest step
        for row in c.execute('SELECT * FROM Rasten WHERE SudID = ?', (id,)):
            s = Step()
            s.name = row[5]
            s.order = order
            s.type = 'A'
            s.state = 'I'
            s.temp = row[3]
            s.timer = row[4]
            s.kettleid = data['mashtun']
            db.session.add(s)
            db.session.commit()
            order +=1

        s = Step()
        s.name = "Laeuterruhe"
        s.order = order
        s.type = 'M'
        s.state = 'I'
        s.temp = 0
        s.timer = 15
        db.session.add(s)
        db.session.commit()
        order +=1

		## Add cooking step
        for row in c.execute('SELECT max(Zeit) FROM Hopfengaben WHERE SudID = ?', (id,)):
            s = Step()
            s.name = "Kochen"
            s.order = order
            s.type = 'A'
            s.state = 'I'
            s.temp = 100
            s.timer = row[0]
            s.kettleid = data["boil"]
            db.session.add(s)
            db.session.commit()
            order +=1

        s = Step()
        s.name = "Whirlpool"
        s.order = order
        s.type = 'M'
        s.state = 'I'
        s.temp = 0
        s.timer = 15
        s.kettleid = data["boil"]
        db.session.add(s)
        db.session.commit()
        order +=1
    except:
        return ('',500)
    finally:
        if conn:
            conn.close()

    return ('',204)

@socketio.on('next', namespace='/brew')
@socketio.on('start', namespace='/brew')
def nextStep():
    active = Step.query.filter_by(state='A').first()
    inactive = Step.query.filter_by(state='I').order_by(Step.order).first()

    if(active != None):
        active.state = 'D'
        active.end = datetime.utcnow()
        setTargetTemp(active.kettleid, 0)
        db.session.add(active)
        db.session.commit()
        app.brewapp_current_step  = None

    if(inactive != None):
        inactive.state = 'A'
        inactive.start = datetime.utcnow()
        setTargetTemp(inactive.kettleid, inactive.temp)
        db.session.add(inactive)
        db.session.commit()
        app.brewapp_current_step  = to_dict(inactive)
        if(inactive.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((inactive.timer_start - datetime(1970,1,1)).total_seconds())*1000

    socketio.emit('step_update', getAsArray(Step), namespace ='/brew')

## WebSocket
@socketio.on('reset', namespace='/brew')
def ws_reset():
    app.brewapp_current_step  = None
    resetSteps()

## Methods
def resetSteps():
    db.session.query(Step).update({'state': 'I', 'start': None, 'end': None, 'timer_start': None},  synchronize_session='evaluate')
    db.session.commit()
    socketio.emit('step_update', getAsArray(Step), namespace ='/brew')

## REST POST PROCESSORS
def post_patch_many(result, **kw):
    pass
    #init()

def post_get(result=None,**kw):
    ## SORT RESULT BY FIELD 'ORDER'
    result["objects"] = sorted(result["objects"], key=lambda k: k['order'])

@brewinit()
def init():
    ## REST API FOR STEP
    manager.create_api(Step, methods=['GET', 'POST', 'DELETE', 'PUT'],allow_patch_many=True, postprocessors={'PATCH_SINGLE': [post_patch_many], 'DELETE_SINGLE': [post_patch_many], 'POST': [post_patch_many],'GET_MANY': [post_get]})
    s = Step.query.filter_by(state='A').first()
    if(s != None):
        app.brewapp_current_step = to_dict(s)
        if(s.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((s.timer_start - datetime(1970,1,1)).total_seconds())*1000


@brewjob(key="stepjob", interval=1)
def stepjob():

    if(app.brewapp_current_step == None):
        return
    cs = app.brewapp_current_step;
    try:
        ct = app.brewapp_kettle_state[cs.get("kettleid")]["temp"]
    except:
        ct = 0

    if(cs.get("timer") > 0 and cs.get("timer_start") == None and ct >= cs.get("temp")):
        s = Step.query.get(cs.get("id"))
        s.timer_start = datetime.utcnow()
        app.brewapp_current_step = to_dict(s)
        if(s.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((s.timer_start - datetime(1970,1,1)).total_seconds())*1000
        db.session.add(s)
        db.session.commit()
        socketio.emit('step_update', getAsArray(Step), namespace ='/brew')

    if(cs.get("type") == 'A' and cs.get("timer_start") != None):

        # check if timer elapsed
        end = cs.get("endunix") + cs.get("timer")*60000
        now = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
        if(end < now):
            nextStep()
