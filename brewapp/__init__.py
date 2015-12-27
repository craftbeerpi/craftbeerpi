from flask import Flask, abort, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask.ext.socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SECRET_KEY'] = 'craftbeerpi'
db = SQLAlchemy(app)

admin = admin.Admin(name="CraftBeerPI")
app.brewapp_jobs = []
app.brewapp_gpio = {}
app.brewapp_chartdata = {}
app.brewapp_temperature = {}
app.testMode = True

from .base.views import base

db.create_all()

admin.init_app(app)

app.register_blueprint(base,url_prefix='/base')

@app.route('/')
def index():
    return redirect('base')

for i in app.brewapp_jobs:
    i()
