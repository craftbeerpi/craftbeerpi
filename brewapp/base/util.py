from brewapp import app, db
from flask_restless.helpers import to_dict
import datetime
import time
from flask import  json
import os.path

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

        return ret
    return wrap

def writeTempToFile(file, timestamp, current_temp, target_temp):
    filename = "log/" + file + ".templog"
    '''

    if os.path.isfile(filename) == False:
        with open(filename, "a") as myfile:
            myfile.write("Date,Current Temperature,Target Temperature\n")
    '''
    formatted_time = datetime.datetime.fromtimestamp((timestamp / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    tt = "0" if target_temp is None else str(target_temp)
    msg = formatted_time + "," + str(current_temp) + "," + tt + "\n"

    with open(filename, "a") as myfile:
        myfile.write(msg)

def writeSpindle(file, timestamp, current_temp, wort, battery):
    filename = "log/" + file + ".templog"

    '''
    if os.path.isfile(filename) == False:
        with open(filename, "a") as myfile:
            myfile.write("Date,Current Temperature,Wort,Battery\n")
    '''
    formatted_time = datetime.datetime.fromtimestamp((timestamp / 1000)).strftime('%Y-%m-%d %H:%M:%S')
    msg = formatted_time + "," + str(current_temp) + "," + str(wort) + "," + str(battery) + "\n"

    with open(filename, "a") as myfile:
        myfile.write(msg)

def read_hydrometer_log(file):

    if os.path.isfile(file) == False:
        return

    import csv
    array = {"hydrometer_temp": [], "wort": [], "battery": []}

    with open(file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #print row
            time = int((datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
            array["hydrometer_temp"].append([time, float(row[1])])
            array["wort"].append([time, float(row[2])])
            array["battery"].append([time, float(row[3])])
    return array


def read_temp_log(file):
    import csv
    result = {"temp": [], "target_temp": []}

    if os.path.isfile(file) == False:
        return result
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #print row
            time = int((datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
            result["temp"].append([time, float(row[1])])

            result["target_temp"].append([time, float(row[2])])
    return result


def delete_file(file):
    if os.path.isfile(file) == True:

        os.remove(file)

from flask import make_response
from functools import wraps, update_wrapper

def updateModel(model, id, json):
    m = model.query.get(id)
    m.decodeJson(json)
    db.session.commit()
    return to_dict(m)

def createModel(model, json):
    m = model()
    m.decodeJson(json)
    db.session.add(m)
    db.session.commit()
    return to_dict(m)

def deleteModel(model, id):
    try:
        model.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except:
        return False


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