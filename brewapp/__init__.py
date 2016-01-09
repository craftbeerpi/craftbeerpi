from flask import Flask, abort, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask.ext.socketio import SocketIO, emit
from thread import start_new_thread
from flask_admin import AdminIndexView, expose
import logging
import flask.ext.restless
from logging.handlers import RotatingFileHandler
import time


app = Flask(__name__)
socketio = SocketIO(app)

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').addHandler(RotatingFileHandler('sqllog.log', maxBytes=10000, backupCount=1))
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
#handler.setLevel(logging.DEBUG)
#app.logger.addHandler(handler)


UPLOAD_FOLDER = './upload'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SECRET_KEY'] = 'craftbeerpi'
app.testMode = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





admin = admin.Admin(name="CraftBeerPI")

## Create Database
db = SQLAlchemy(app)
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
## Import modules (Flask Blueprints)
from .base.views import base
#from .log.views import log


## Create Database
db.create_all()


## REST


## Init Admin Components
admin.init_app(app)

## Register modules (Flask Blueprints)
app.register_blueprint(base,url_prefix='/base')






@app.route('/')
def index():
    #from brewapp.base.model import Kettle2
    #c = Kettle2.query.count()
    #if(c == 0):
    #    return redirect('kettle')
    #else:
    return redirect('base')



print "INIT METHODS"
for i in app.brewapp_init:
    name = i.__name__
    print "--> ", name
    i()


def job(key, interval, method):
    while app.brewapp_jobstate2[key]:
        method()
        time.sleep(interval)

print "INIT JOBS2"
for i in app.brewapp_jobs2:
    app.brewapp_jobstate2[i.get("key")] = True

    start_new_thread(job,(i.get("key"),i.get("interval"),i.get("function")))
    print "--> ", i.get("function").__name__
