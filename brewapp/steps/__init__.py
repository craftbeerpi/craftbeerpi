import step
import admin
from views import steps
from brewapp import app
app.register_blueprint(steps,url_prefix='/steps')
