from brewapp import app,socketio
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.socketio import SocketIO, emit
from flask.ext.babel import Babel

if __name__ == "__main__":

    app.debug = True
    app.config['SECRET_KEY'] = 'craftbeerpi'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['BABEL_DEFAULT_LOCALE'] = 'de'
    babel = Babel(app)
    toolbar = DebugToolbarExtension(app)
    socketio.run(app, host='0.0.0.0', use_reloader=False)
