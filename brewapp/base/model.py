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
    vesselid = db.Column(db.Integer())

    def __repr__(self):
        return '<Step %r>' % self.name

    def __unicode__(self):
        return self.id

class Vessel2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sensorid = db.Column(db.String(80))
    heater = db.Column(db.Integer())
    agitator = db.Column(db.Integer())
    target_temp = db.Column(db.Integer())
    height = db.Column(db.Integer())
    diameter = db.Column(db.Integer())

    def __repr__(self):
        return '<Vessel %r>' % self.name

    def __unicode__(self):
        return self.id

class VesselTempLog2(db.Model):
    vesselid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(), primary_key=True)
    value = db.Column(db.Float())
