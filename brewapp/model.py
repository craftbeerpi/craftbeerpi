from brewapp import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os.path as op
import json

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
            "temp1": [self.to_unixTime(self.time),self.value1],
            "temp2": [self.to_unixTime(self.time),self.value2],
            "temp3": [self.to_unixTime(self.time),self.value3],
            "temp4": [self.to_unixTime(self.time),self.value4],
            "temp5": [self.to_unixTime(self.time),self.value5],
        }


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

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))

    config_cache = {}

    def __repr__(self):
        return '<Config %r>' % self.value

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value
        }

    @staticmethod
    def getParameter(parameter_name, default, isJson=False):

        result = None
        if(Config.config_cache.get(parameter_name) != None):
            result = Config.config_cache.get(parameter_name);

        else:
            # Try to read from db
            c = Config.query.filter_by(name=parameter_name).first()
            if(c == None):
                result = default
            else:
                Config.config_cache[parameter_name] = c.value
                result = c.value

        try:
            if(isJson == True):
                return json.loads(result)
            elif(type(default) is str):
                return str(result)
            elif(type(default) is float):
                return float(result)
            elif(type(default) is int):
                return int(result)
            elif(type(default) is bool):
                return str2bool(result)
        except:
            if(isJson == True):
                return json.loads(default)
            else:
                return default

    @staticmethod
    def setParameter(config):
        Config.config_cache[config.name] = config.value

    @staticmethod
    def clearParameter(parameter_name):
        config_cache[parameter_name] = None


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def getAsArray(obj):
    steps=obj.query.all()
    ar = []
    for t in steps:
        ar.append(t.to_json())
    return ar

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
    db.session.commit()

def addConfig(name, value):
    c = Config()
    c.name = name
    c.value =value
    db.session.add(c)
    db.session.commit()

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

    addConfig("gpio_heat","{\"label\": \"Heizung\", \"pin\": 6}")
    addConfig("gpio_agitator","{\"label\": \"Ruehrwerk\", \"pin\": 6}")
    addConfig("pid_agitator", "True")
    addConfig("temp_db_interval", "5")
    addConfig("brew_name", "Beispiel Sud")
    addConfig("tempSensorId1", "{\"name\": \"P22\", \"id\": \"28-03146215acff\"}")
