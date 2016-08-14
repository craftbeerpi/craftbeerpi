from flask import Flask, abort, redirect, url_for, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from thread import start_new_thread
import logging
import flask_restless
from logging.handlers import RotatingFileHandler
import time
import os
from brewapp import app


import inspect
from functools import wraps
## SECURTIY

def requires_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@requires_auth
def detect_user_language():
    pass

def check_auth(username, password):
    return username == app.brewapp_config["USERNAME"] and password == app.brewapp_config["PASSWORD"]

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


