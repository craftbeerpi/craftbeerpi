from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from wtforms.fields import SelectField
from model import *

class ClearLogs2(BaseView):
    @expose('/')
    def index(self):
        clearData()
        return self.render('admin/reset_protocol_result.html')


def clearData():
    Log.query.delete()
    db.session.commit()
    app.brewapp_log = []

admin.add_view(ClearLogs2(name="Clear All Log", category='Logs'))
