from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from model import *
from wtforms.fields import SelectField
from views import initKettle


class KettleAdmin(sqla.ModelView):
	form_columns = ['name','sensorid', 'heater', 'agitator', 'height', 'diameter']
	def after_model_change(self, form, model, is_created):
		initKettle()
		pass


class Kettle2Setup(BaseView):
    @expose('/')
    def index(self):
		mt = Kettle()
		mt.name = "MashTun"
		mt.sensorid = "28-03146215acff"
		mt.heater = 23
		mt.agitator = None
		db.session.add(mt)

		hlt = Kettle()
		hlt.name = "Hot Liquor Tank"
		hlt.sensorid = None
		hlt.heater = None
		db.session.add(hlt)

		bt = Kettle()
		bt.name = "Boil Tank"
		bt.sensorid = "None"
		bt.heater = "None"
		db.session.add(bt)
		db.session.commit()
		initKettle()
		return self.render('admin/reset_protocol_result.html')





admin.add_view(KettleAdmin(Kettle, db.session, name="KettleConfig", category='Kettle'))
admin.add_view(Kettle2Setup(name="KettleSetup", category='Kettle'))
