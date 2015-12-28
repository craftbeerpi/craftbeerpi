from brewapp import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op
import json


class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime())
    value1 = db.Column(db.Float())
    value2 = db.Column(db.Float())
    value3 = db.Column(db.Float())
    value4 = db.Column(db.Float())
    value5 = db.Column(db.Float())

    def __repr__(self):
        return '<Temp %r>' % self.id

    def __unicode__(self):
        return self.id

    def to_json(self):
        return {
            "temp1": [self.to_unixTime(),self.value1],
            "temp2": [self.to_unixTime(),self.value2],
            "temp3": [self.to_unixTime(),self.value3],
            "temp4": [self.to_unixTime(),self.value4],
            "temp5": [self.to_unixTime(),self.value5],
        }


    def to_unixTime(self):
        return  int((self.time - datetime(1970,1,1)).total_seconds())*1000

class ThermometerConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    gpio = db.Column(db.Integer)

    def __repr__(self):
        return '<Step %r>' % self.name

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'name' : self.name,
            'gpio' : self.gpio,
        }
