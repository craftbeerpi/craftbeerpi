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

    def __repr__(self):
        return '<Step %r>' % self.name

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'type' : self.type,
            'name' : self.name,
            'timer' : self.timer,
            'temp' : self.temp,
            'state': self.state,
            'start': str(self.start),
            'start2': self.to_unixTime(self.start),
            'end': str( self.end),
            'end2': self.to_unixTime(self.end),
            'timer_start' : self.to_unixTime(self.timer_start),

        }

    def to_unixTime(self, field):
        if(field!= None):
            return  int((field - datetime(1970,1,1)).total_seconds())*1000
        else:
            return  None

class GpioConfig(db.Model):
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

def nextStep():
    active = Step.query.filter_by(state='A').first()
    inactive = Step.query.filter_by(state='I').order_by(Step.order).first()

    if(active != None):
        active.state = 'D'
        active.end = datetime.utcnow()
        db.session.add(active)
        db.session.commit()

    if(inactive != None):
        inactive.state = 'A'
        inactive.start = datetime.utcnow()
        db.session.add(inactive)
        db.session.commit()
