from brewapp import app
from flask.ext.restless.helpers import to_dict

def getAsArray(obj, order = None):
    if(order is not None):
        result =obj.query.order_by(order).all()
    else:
        result =obj.query.all()
    ar = []
    for t in result:
        ar.append(to_dict(t))
    return ar

def getAsDict(obj, key, order = None):
    if(order is not None):
        result =obj.query.order_by(order).all()
    else:
        result =obj.query.all()
    ar = {}
    for t in result:
        ar[getattr(t, key)] = t.to_json()
    return ar

def setTargetTemp(kettleid, temp):
    if(kettleid == None):
        return
    if(app.brewapp_target_temp_method != None):
        app.brewapp_target_temp_method(kettleid, temp)

## Job Annotaiton
## key = uniquie key as string
## interval = interval in which the method is invoedk
def brewjob(key, interval):
    def real_decorator(function):
        app.brewapp_jobs.append({"function": function, "key": key, "interval": interval})
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return real_decorator

## Init Annotaiton
def brewinit():
    def real_decorator(function):
        app.brewapp_init.append(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator

def brewstepaction():
    def real_decorator(function):
        app.brewapp_stepaction.append(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator

def brewautomatic():
    def real_decorator(function):
        app.brewapp_pid.append(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator
