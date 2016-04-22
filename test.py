from flask import json
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

automatics = {}

def automatic():

    def hallo1(function):
        automatics[function.__name__] = function
        print "AUTOMATIC" ,function.__name__
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return hallo1

def run():
    def hallo1(function):
        print "FUNCTION" ,function.__name__
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return hallo1


class PIDbase(object):
    paramter = None

@automatic()
class test(PIDbase):

    paramter = ["p","i","d"]

    def run(self):
        print self.paramter
        print "RUNNING11"


class Config(Base):
    __tablename__ = 'config'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    key = Column(String(20), nullable=False)
    value = Column(String(255))

engine = create_engine('sqlite:///../example.db')

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_person = Config(key='hallo')

new_person.value = json.dumps(["a","b"])
#session.add(new_person)
#session.commit()

c = session.query(Config).first()

print json.loads(c.value)[1]
#a = automatics["test"]()

#print "JSON"

#print json.dumps(a.paramter)
