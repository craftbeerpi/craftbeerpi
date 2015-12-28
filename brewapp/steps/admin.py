from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from brewapp.steps.model import Step
from wtforms.fields import SelectField
from step import init


class StepsAdmin(sqla.ModelView):
	form_columns = ['name', 'temp', 'timer', 'type','state','timer_start','start','end','order']
	form_overrides = dict(state=SelectField, type=SelectField, stir_heatup=SelectField)
	form_args = dict(
		state=dict(choices=[("I", 'Inaktiv'), ("A", 'Aktiv'), ("D", 'Fertig')],),
		type=dict(choices=[("A", 'Automatisch'), ("M", 'Manuell')],)
		)
	column_default_sort = 'order'
	def after_model_change(self, form, model, is_created):
		init()
		pass
        #current_step = Step.query.filter_by(state='A').first()
        #print current_step
        #if(current_step != None):
        #   app.brewapp_current_step = current_step.to_json()
        #else:
        #    app.brewapp_current_step = None


admin.add_view(StepsAdmin(Step, db.session, name="Steps"))
