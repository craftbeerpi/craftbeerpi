from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from model import *
from wtforms.fields import SelectField
from views import initVessel


class VesselAdmin(sqla.ModelView):
	form_columns = ['name','sensorid', 'heater', 'agitator']
	def after_model_change(self, form, model, is_created):
		initVessel()
		pass


class Vessel2Setup(BaseView):
    @expose('/')
    def index(self):
		mt = Vessel()
		mt.name = "MashTun"
		mt.sensorid = "ABC"
		mt.heater = 22
		mt.agitator = 23
		db.session.add(mt)

		hlt = Vessel()
		hlt.name = "Hot Liquor Tank"
		hlt.sensorid = "ABC"
		hlt.heater = 24
		db.session.add(hlt)

		bt = Vessel()
		bt.name = "Boil Tank"
		bt.sensorid = "ABC"
		bt.heater = 25
		db.session.add(bt)
		db.session.commit()
		initVessel()
		return self.render('admin/reset_protocol_result.html')

class ClearTemperatureLog(BaseView):
    @expose('/')
    def index(self):
		VesselTempLog.query.delete()
		db.session.commit()
		app.brewapp_vessel_temps_log = {}
		for vid in app.brewapp_vessel:
			app.brewapp_vessel_temps_log[vid] = []
		return self.render('admin/reset_protocol_result.html')


admin.add_view(VesselAdmin(Vessel, db.session, name="VesselConfig", category='Vessel'))
admin.add_view(Vessel2Setup(name="VesselSetup", category='Vessel'))
admin.add_view(ClearTemperatureLog(name="Clear Temperature Log", category='Temperature'))
