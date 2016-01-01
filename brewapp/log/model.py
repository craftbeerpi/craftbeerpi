from brewapp import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op
import json


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    time = db.Column(db.DateTime())
    type = db.Column(db.String(1))


    def __repr__(self):
        return '<Log %r>' % self.text

    def __unicode__(self):
        return self.text

    def to_json(self):
        return {
            'time': self.to_unixTime(self.time),
            'text': self.text,
            'type': self.type
        }

    def to_unixTime(self, field):
        if(field!= None):
            return  int((field - datetime(1970,1,1)).total_seconds())*1000
        else:
            return  None
