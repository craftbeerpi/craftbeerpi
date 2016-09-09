from brewapp import app
from flask_restless.helpers import to_dict
import datetime
import time
def getAsArray(obj, order = None):
    if order is not None :
        result =obj.query.order_by(order).all()
    else:
        result =obj.query.all()
    ar = []
    for t in result:
        ar.append(to_dict(t))
    return ar


def getAsDict(obj, key, deep=None, order = None):
    if order is not None :
        result = obj.query.order_by(order).all()
    else:
        result =obj.query.all()
    ar = {}
    for t in result:
        ar[getattr(t, key)] = to_dict(t, deep=deep)
    return ar


def setTargetTemp(kettleid, temp):
    if kettleid is None:
        return
    if app.brewapp_target_temp_method is not None:
        app.brewapp_target_temp_method(kettleid, temp)


# Job Annotaiton
# key = uniquie key as string
# interval = interval in which the method is invoedk
def brewjob(key, interval, config_parameter = None):
    def real_decorator(function):
        app.brewapp_jobs.append({"function": function, "key": key, "interval": interval, "config_parameter": config_parameter})
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return real_decorator


# Init Annotaiton
def brewinit(order = 0, config_parameter = None):
    def real_decorator(function):
        app.brewapp_init.append({"function": function, "order": order, "config_parameter": config_parameter})
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator


def config(name):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if(app.brewapp_config.get(name, 'No') == 'Yes'):
                function(*args, **kwargs)
            else:
                pass
        return wrapper

    return real_decorator

def brewautomatic():
    def real_decorator(function):
        app.brewapp_pid.append(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator

def controllerLogic():
    def real_decorator(function):
        app.brewapp_controller[function.__name__] = function
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper

    return real_decorator

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def writeTempToFile(file, timestamp, current_temp, target_temp):
    formatted_time = datetime.datetime.fromtimestamp((timestamp / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    tt = "0" if target_temp is None else str(target_temp)
    msg = formatted_time + "," + str(current_temp) + "," + tt + "\n"
    filename = "log/" + file + ".templog"
    with open(filename, "a") as myfile:
        myfile.write(msg)