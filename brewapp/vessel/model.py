from brewapp import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op
import json


class Vessel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sensorid = db.Column(db.String(80))
    heater = db.Column(db.Integer())
    agitator = db.Column(db.Integer())
    target_temp = db.Column(db.Integer())
    height = db.Column(db.Integer())
    diameter = db.Column(db.Integer())

    def __repr__(self):
        return '<Temp %r>' % self.id

    def __unicode__(self):
        return self.id

    def to_json(self):
        return {
            'id': self.id,
            'name' : self.name,
            'sensorid' : self.sensorid,
            'heater' : {"gpio": self.heater, "state": False},
            'agitator' : {"gpio": self.agitator, "state": False},
            'automatic' : False,
            'target_temp': self.target_temp,
            'height' : self.height,
            'diameter' : self.diameter,
        }


    def to_unixTime(self):
        return  int((self.time - datetime(1970,1,1)).total_seconds())*1000

class VesselTempLog(db.Model):
    vesselid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(), primary_key=True)
    value = db.Column(db.Float())


    def to_unixTime(self):
        return  int((self.time - datetime(1970,1,1)).total_seconds())*1000

    def to_json(self):
        return [self.to_unixTime(),self.value]
