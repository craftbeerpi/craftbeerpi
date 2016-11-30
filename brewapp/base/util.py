from brewapp import app
from flask_restless.helpers import to_dict
import datetime
import time
from flask import  json

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

def writeSpindle(file, timestamp, current_temp, angle, battery):
    formatted_time = datetime.datetime.fromtimestamp((timestamp / 1000)).strftime('%Y-%m-%d %H:%M:%S')

    msg = formatted_time + "," + str(current_temp) + "," + str(angle) + "," + str(battery) + "\n"
    filename = "log/" + file + ".templog"
    with open(filename, "a") as myfile:
        myfile.write(msg)


def read_temp_log(file):
    import csv
    array = {"temp": [], "target_temp": []}
    print file
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #print row
            time = int((datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
            array["temp"].append([time, float(row[1])])

            array["target_temp"].append([time, float(row[2])])
    return json.dumps(array)

from flask import make_response
from functools import wraps, update_wrapper


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)