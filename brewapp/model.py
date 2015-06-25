from brewapp import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
db = SQLAlchemy(app)


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
    stir_interval = db.Column(db.Integer())
    stir_time = db.Column(db.Integer())

    def __repr__(self):
        return '<Step %r>' % self.name

    def __unicode__(self):
        return self.name

    def to_json(self):


        return {
            'type' : self.type,
            'name' : self.name,
            'timer' : str(self.timer),
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

class Temperatur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime())
    name1 = db.Column(db.String(80))
    value1 = db.Column(db.Float())
    name2 = db.Column(db.String(80))
    value2 = db.Column(db.Float())
    name3 = db.Column(db.String(80))
    value3 = db.Column(db.Float())
    name4 = db.Column(db.String(80))
    value4 = db.Column(db.Float())
    name5 = db.Column(db.String(80))
    value5 = db.Column(db.Float())

    def __repr__(self):
        return '<Log %r>' % self.name1

    def __unicode__(self):
        return self.name1

    def to_json(self):
        return [
           self.to_unixTime(self.time),
           self.value1
        ]

    def to_unixTime(self, field):
        if(field!= None):
            return  int((field - datetime(1970,1,1)).total_seconds())*1000
        else:
            return  None

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

#class Sud(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    time = db.Column(db.DateTime())
#    type = db.Column(db.String(1))
#    text = db.Column(db.String(255))
#
#
#    def __repr__(self):
#        return '<Log %r>' % self.text
#
#    def __unicode__(self):
#        return self.text

## Drop all tables
#db.drop_all()

## Helper Method
def addStep(order, name, temp, type, timer, state='I'):
    s = Step()
    s.order = order
    s.name = name
    s.temp = temp
    s.type = type
    s.timer = timer
    s.state = state
    db.session.add(s)

db_exists = op.isfile("craftbeerpi.db") 
## Create db model
db.create_all()

if(db_exists == False):
    ## DUMMY DATA
    print "IMPORT DUMMY STEPS"
    addStep(0, 'Einmaischen', 45.0, 'M', 10)
    addStep(1, 'Eiweisrast', 43.0, 'A', 20)
    addStep(2, 'Maltoserast', 62.0, 'A', 30)
    addStep(3, 'Verzuckerung', 73.0, 'A', 30)
    addStep(4, 'Abmaischen', 78.0, 'M', 1)
    addStep(5, 'Laeutern', 0, 'M', 0)
    addStep(6, 'Laeutern Ruhe', 0, 'A', 15)
    addStep(7, 'Vorderwuerzehopfung', 0, 'M', 10)
    addStep(8, 'Kochen', 99, 'A', 90)
    addStep(9, 'Kuehlen', 23, 'M', 20)
    db.session.commit()
    