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

def addLogMessage(message):
    if(app.brewapp_log_method != None):
        app.brewapp_log_method(message)

def setTargetTemp(vesselid, temp):
    if(vesselid == None):
        return
    if(app.brewapp_target_temp_method != None):
        app.brewapp_target_temp_method(vesselid, temp)



def brewjob(key, interval):
    def real_decorator(function):
        app.brewapp_jobs2.append({"function": function, "key": key, "interval": interval})
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator

def brewinit():
    def real_decorator(function):

        app.brewapp_init.append(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator
