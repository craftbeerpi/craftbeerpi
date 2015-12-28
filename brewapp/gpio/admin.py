from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from brewapp.gpio.model import GpioConfig
from wtforms.fields import SelectField
from brewapp.gpio.gpio import setupGPIO



class GpioAdmin(sqla.ModelView):
	form_columns = ['name','gpio']
	def after_model_change(self, form, model, is_created):
		setupGPIO()
		pass

admin.add_view(GpioAdmin(GpioConfig, db.session, name="GPIO", category='Config'))
