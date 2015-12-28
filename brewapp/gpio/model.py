from brewapp import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op
import json

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
