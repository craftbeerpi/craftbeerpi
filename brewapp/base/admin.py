from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from model import *
from wtforms.fields import SelectField
from thermometer import clearData

class TemperatureAdmin(sqla.ModelView):
	form_columns = ['time','value1']

class GpioAdmin(sqla.ModelView):
	form_columns = ['name','gpio']

class StepsAdmin(sqla.ModelView):
	form_columns = ['name', 'temp', 'timer', 'type','state','timer_start','start','end','order']
	form_overrides = dict(state=SelectField, type=SelectField, stir_heatup=SelectField)
	form_args = dict(
		state=dict(choices=[("I", 'Inaktiv'), ("A", 'Aktiv'), ("D", 'Fertig')],),
		type=dict(choices=[("A", 'Automatisch'), ("M", 'Manuell')],)
		)
	column_default_sort = 'order'
	def after_model_change(self, form, model, is_created):
		print "JOB UPDATE"
		app.brewapp_current_step = model.to_json()
		pass
        #current_step = Step.query.filter_by(state='A').first()
        #print current_step
        #if(current_step != None):
        #   app.brewapp_current_step = current_step.to_json()
        #else:
        #    app.brewapp_current_step = None
class ClearLogs(BaseView):
    @expose('/')
    def index(self):
        clearData()
        return self.render('admin/reset_protocol_result.html')

admin.add_view(GpioAdmin(GpioConfig, db.session, name="GPIO", category='Config'))
admin.add_view(StepsAdmin(Step, db.session, name="Steps"))
admin.add_view(TemperatureAdmin(Temperature, db.session, name="Temperature Log", category='Protocol'))
admin.add_view(ClearLogs(name="Clear All Data", category='Protocol'))
admin.add_link(base.MenuLink("Back", url="/"))
