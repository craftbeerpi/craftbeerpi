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
from flask.ext.restless.helpers import to_dict
import StringIO
import csv
import datetime
from flask import make_response, Response

@brewinit()
def init():
    manager.create_api(RecipeBooks, methods=['GET', 'POST', 'DELETE', 'PUT'])
    manager.create_api(RecipeBookSteps, methods=['GET', 'POST', 'DELETE', 'PUT'])

@app.route('/api/recipe_books/load/<id>', methods=['POST'])
def loadRecipe(id):

    Step.query.delete()
    db.session.commit()
    print id
    recipe = RecipeBooks.query.get(id);

    for a in recipe.steps:
        s = Step(name=a.name, order=a.order, timer=a.timer, temp=a.temp, type=a.type, state="I", kettleid=a.kettleid)
        db.session.add(s)
        db.session.commit()

    setBrewName(recipe.name)
    return ('',204)

@app.route('/api/recipe_books/export')
def export_book():
    r = RecipeBooks.query.all()
    ar = []
    for t in r:
        ar.append(to_dict(t,  deep={'steps': []}))

    return Response(json.dumps(ar),
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=CraftBeerPI_RecipeBook.json'})



@app.route('/api/recipe_books/save', methods=['POST'])
def save_book():
    data =request.get_json()

    recipie = RecipeBooks.query.filter_by(name=data["name"]).first()

    if(recipie != None):
        db.session.delete(recipie)
        db.session.commit()

    s = Step.query.all()
    steps = []
    for a in s:
        steps.append(RecipeBookSteps(name=a.name, order=a.order, timer=a.timer, temp=a.temp, type=a.type, kettleid=a.kettleid))

    rb = RecipeBooks(name=data["name"], steps=steps)
    db.session.add(rb)
    db.session.commit()
    return ('',204)



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
