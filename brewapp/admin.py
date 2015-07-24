import flask_admin as admin
from brewapp import app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from admin import *
from model import *
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
import os
from flask_admin import BaseView, expose
import sqlite3
from flask import Flask, redirect, request, url_for
from werkzeug import secure_filename
from brewapp.model import db, Step, Temperatur, Log, Config
from flask.ext.admin import base
import globalprops
from wtforms.fields import SelectField

## Standard Admin UI for Database models
class StepAdmin(sqla.ModelView):
	form_columns = ['name', 'temp', 'timer', 'type','state','timer_start','start','end','order']
	form_overrides = dict(state=SelectField, type=SelectField, stir_heatup=SelectField)
	form_args = dict(state=dict(choices=[("I", 'Inaktiv'), ("A", 'Aktiv'), ("D", 'Fertig')],),
		type=dict(choices=[("A", 'Automatisch'), ("M", 'Manuell')],))

class TempAdmin(sqla.ModelView):
	form_columns = ['time', 'value1']

class LogAdmin(sqla.ModelView):
	form_columns = ['time', 'text', 'type']

class ConfigAdmin(sqla.ModelView):
	form_columns = ['name', 'value']
	column_searchable_list = ['name']

	def after_model_change(self, form, model, is_created):
		Config.setParameter(model)
		pass

## Admin View to select a brew
class KBSelect(BaseView):
    @expose('/')
    def index(self):
    	arr = []
    	try:
        	conn = sqlite3.connect('./brewapp/dbimport/import.db')
        	c = conn.cursor()
        	for row in c.execute('SELECT * FROM Sud'):
        		arr.append(row)
        except:
        	pass
        return self.render('admin/imp.html', x= arr)

    # Import brew from kleiner brauhelfer
    @expose('/select')
    def select(self):
    	## delete current brew
		Step.query.delete()
		db.session.commit()


		id = request.args.get("id")
		conn = sqlite3.connect('./brewapp/dbimport/import.db')
		c = conn.cursor()
		order = 0

		### Add einmaisch step
		for row in c.execute('SELECT EinmaischenTemp, Sudname FROM Sud WHERE ID = ?', id):
			s = Step()
			s.name = "Einmaischen"
			s.order = order
			s.type = 'M'
			s.state = 'I'
			s.temp = row[0]
			s.timer = 0
			db.session.add(s)
			db.session.commit()

			brew_name = Config.query.filter_by(name='brew_name').first()
			if(brew_name == None):
				brew_name = Confg()
				brew_name.name = "brew_name"
				brew_name.value = row[1]
			else:
				brew_name.value = row[1]
			Config.setParameter(brew_name)
			db.session.add(brew_name)
			db.session.commit()

			order +=1

		### add rest step
		for row in c.execute('SELECT * FROM Rasten WHERE SudID = ?', id):
			s = Step()
			s.name = row[5]
			s.order = order
			s.type = 'A'
			s.state = 'I'
			s.temp = row[3]
			s.timer = row[4]
			db.session.add(s)
			db.session.commit()
			order +=1

		## Add cooking step
		for row in c.execute('SELECT max(Zeit) FROM Hopfengaben WHERE SudID = ?', id):
			s = Step()
			s.name = "Kochen"
			s.order = order
			s.type = 'A'
			s.state = 'I'
			s.temp = 100
			s.timer = row[0]
			db.session.add(s)
			db.session.commit()
			order +=1

		return self.render('admin/imp_result.html')

## View to import database from kleiner brauhelfer
class KBUpload(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/kb_upload.html')

    @expose('/upload',methods=('POST', ))
    def upload(self):
    	if request.method == 'POST':
    		file = request.files['file']
    		filename = secure_filename(file.filename)
    		file.save(os.path.join('./brewapp/dbimport/', 'import.db'))
        	return self.render('admin/imp_result.html')

class ClearLogs(BaseView):

    @expose('/')
    def index(self):
		Log.query.delete()
		db.session.commit()
		Temperatur.query.delete()
		db.session.commit()
		globalprops.chart_cache =  { }
		return self.render('admin/imp_result.html')

## Register Views

admin = admin.Admin(name="CraftBeerPI")
admin.add_link(base.MenuLink("Back", url="/"))
admin.add_view(StepAdmin(Step, db.session, name="Brew Steps"))
admin.add_view(TempAdmin(Temperatur, db.session, name="Temperature Log", category='Protocol'))
admin.add_view(LogAdmin(Log, db.session, name="Brew Protocol", category='Protocol'))
admin.add_view(ClearLogs(name="Clear All Data", category='Protocol'))
admin.add_view(ConfigAdmin(Config, db.session, name="Configuration"))
admin.add_view(KBSelect(name='Recipe List', category='Kleiner Brauhelfer'))
admin.add_view(KBUpload(name='Upload', category='Kleiner Brauhelfer'))

admin.init_app(app)
