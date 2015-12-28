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
            'id': self.id,
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
