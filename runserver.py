from flask import Flask
from brewapp import app, socketio
from flask.ext.socketio import SocketIO, emit
#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    
    #app.run()
    socketio.run(app, host='0.0.0.0', use_reloader=False)
