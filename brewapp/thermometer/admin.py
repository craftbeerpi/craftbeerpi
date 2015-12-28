from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from brewapp.thermometer.model import Temperature, ThermometerConfig
from wtforms.fields import SelectField
from thermometer import clearData, loadThermometer

class TemperatureAdmin(sqla.ModelView):
	form_columns = ['time','value1']

class ClearLogs(BaseView):
    @expose('/')
    def index(self):
        clearData()
        return self.render('admin/reset_protocol_result.html')


class ThermometerConfigAdmin(sqla.ModelView):
	form_columns = ['name','gpio']
	def after_model_change(self, form, model, is_created):
		loadThermometer()
		pass

admin.add_view(ThermometerConfigAdmin(ThermometerConfig, db.session, name="Thermometer", category='Config'))
admin.add_view(TemperatureAdmin(Temperature, db.session, name="Temperature Log", category='Protocol'))
admin.add_view(ClearLogs(name="Clear All Data", category='Protocol'))
