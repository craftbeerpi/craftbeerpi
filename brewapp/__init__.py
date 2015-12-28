from flask import Flask, abort, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask.ext.socketio import SocketIO, emit
from thread import start_new_thread

def brewjob(key):
    def real_decorator(function):
        app.brewapp_jobs.append({"function": function, "key": key})
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator


def brewinit():
    def real_decorator(function):

        app.brewapp_init.append(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SECRET_KEY'] = 'craftbeerpi'
db = SQLAlchemy(app)

admin = admin.Admin(name="CraftBeerPI")
app.brewapp_jobs = []
app.brewapp_init = []
app.brewapp_gpio = {}
app.brewapp_chartdata = {}
app.brewapp_temperature = {}
app.testMode = True
app.brewapp_jobstate = {}
app.brewapp_current_step = None

from .base.views import base

db.create_all()

admin.init_app(app)

app.register_blueprint(base,url_prefix='/base')

@app.route('/')
def index():
    return redirect('base')

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
