#!/usr/bin/env python

from flask import Flask
from brewapp import app, socketio
from flask.ext.socketio import SocketIO, emit


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0', use_reloader=False)
