from util import *
from model import *
from brewapp import app, socketio
from brewapp import manager
from flask.ext.restless.helpers import to_dict
import json
from flask import request

@brewinit()
def init():
    print "FERMENTER"
    manager.create_api(Fermenter, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/api/fermenter/<id>/targettemp', methods=['POST'])
def setTargetTempFermenter(id):
    print "SET TT F"
    id = int(id)
    data =request.get_json()
    temp = int(data["temp"])
    setTargetTemp(id,temp)
    return ('',204)

def setTargetTemp(id, temp):
    fermenter = Fermenter.query.get(id)
    if(fermenter != None):
        fermenter.target_temp = temp
        db.session.add(fermenter)
        db.session.commit()
        print "DONE"
        #app.brewapp_kettle_state[id]["target_temp"] = temp
        socketio.emit('fermenter_update', getAsArray(Fermenter), namespace ='/brew')