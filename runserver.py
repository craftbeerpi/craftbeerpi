from brewapp import app,socketio 
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.socketio import SocketIO, emit

if __name__ == "__main__":

    app.debug = False
    app.config['SECRET_KEY'] = 'WOOHOO'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    toolbar = DebugToolbarExtension(app)
    socketio.run(app, host='0.0.0.0', use_reloader=False)

