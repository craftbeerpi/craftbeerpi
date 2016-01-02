from flask import Flask, abort, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask.ext.socketio import SocketIO, emit
from thread import start_new_thread

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SECRET_KEY'] = 'craftbeerpi'
app.testMode = True
admin = admin.Admin(name="CraftBeerPI")

## Create Database
db = SQLAlchemy(app)

## Import modules (Flask Blueprints)
from .base.views import base
from .steps.views import steps
from .formulas.views import formulas
#from .log.views import log
from .vessel.views import vessel
## Create Database
db.create_all()
## Init Admin Components
admin.init_app(app)

## Register modules (Flask Blueprints)
app.register_blueprint(base,url_prefix='/base')
app.register_blueprint(steps,url_prefix='/steps')
app.register_blueprint(formulas,url_prefix='/formulas')
#app.register_blueprint(log,url_prefix='/log')
app.register_blueprint(vessel,url_prefix='/vessel')

@app.route('/')
def index():
    return redirect('vessel')

print "INIT METHODS"
for i in app.brewapp_init:
    name = i.__name__
    print "--> ", name
    i()

print "INIT JOBS"
for i in app.brewapp_jobs:
    app.brewapp_jobstate[i.get("key")] = True
    start_new_thread(i.get("function"),())
    print "--> ", i.get("function").__name__
