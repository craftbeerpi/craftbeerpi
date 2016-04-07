from brewapp import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op
import json

class Step(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order = db.Column(db.Integer())
    temp = db.Column(db.Float())
    name = db.Column(db.String(80))
    timer = db.Column(db.Integer())
    type = db.Column(db.String(1))
    state = db.Column(db.String(1))
    timer_start = db.Column(db.DateTime())
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    kettleid = db.Column(db.Integer())

    def __repr__(self):
        return '<Step %r>' % self.name

    def __unicode__(self):
        return self.id

class Kettle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sensorid = db.Column(db.String(80))
    sensoroffset = db.Column(db.Float())
    heater = db.Column(db.String(10))
    automatic = db.Column(db.String(255))
    agitator = db.Column(db.String(10))
    target_temp = db.Column(db.Integer())
    height = db.Column(db.Integer())
    diameter = db.Column(db.Integer())

    def __repr__(self):
        return '<Kettle %r>' % self.name

    def __unicode__(self):
        return self.id

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    switch = db.Column(db.String(80))

class Config(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    type = db.Column(db.String(50))
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return '<Config %r>' % self.name

    def __unicode__(self):
        return self.name
