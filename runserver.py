#!/usr/bin/env python

from flask import Flask
from brewapp import app, socketio
from flask_socketio import SocketIO, emit
from flask_debugtoolbar import DebugToolbarExtension



if __name__ == '__main__':
    app.debug = False
    #toolbar = DebugToolbarExtension(app)

    socketio.run(app, host='0.0.0.0')
