from admin import *
from brewapp import admin, db, app
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import BaseView, expose
from flask.ext.admin import base
from brewapp.steps.model import Step
from wtforms.fields import SelectField
from step import init
from flask import Flask, redirect, request, url_for
from werkzeug import secure_filename
import os.path as op
import os
import sqlite3

class StepsAdmin(sqla.ModelView):
	form_columns = ['name', 'temp', 'timer', 'type','state','timer_start','start','end','order', 'vesselid']
	form_overrides = dict(state=SelectField, type=SelectField, stir_heatup=SelectField)
	form_args = dict(
		state=dict(choices=[("I", 'Inaktiv'), ("A", 'Aktiv'), ("D", 'Fertig')],),
		type=dict(choices=[("A", 'Automatisch'), ("M", 'Manuell')],)
		)
	column_default_sort = 'order'
	def after_model_change(self, form, model, is_created):
		init()
		pass

class KBSelect(BaseView):
    @expose('/')
    def index(self):
    	arr = []
        conn = sqlite3.connect("./import.db")
        c = conn.cursor()
        for row in c.execute('SELECT * FROM Sud'):
        	arr.append(row)

        return self.render('admin/imp.html', x= arr)

    # Import brew from kleiner brauhelfer
    @expose('/select')
    def select(self):
    	## delete current brew
		Step.query.delete()
		db.session.commit()

		id = request.args.get("id")
		conn = sqlite3.connect('./import.db')
		c = conn.cursor()
		order = 0

		### Add einmaisch step
		for row in c.execute('SELECT EinmaischenTemp, Sudname FROM Sud WHERE ID = ?', (id,)):
			s = Step()
			s.name = "Einmaischen"
			s.order = order
			s.type = 'M'
			s.state = 'I'
			s.temp = row[0]
			s.timer = 0
			db.session.add(s)
			db.session.commit()

			order +=1

		### add rest step
		for row in c.execute('SELECT * FROM Rasten WHERE SudID = ?', (id,)):
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

		s = Step()
		s.name = "Laeuterruhe"
		s.order = order
		s.type = 'M'
		s.state = 'I'
		s.temp = 0
		s.timer = 15
		db.session.add(s)
		db.session.commit()
		order +=1

		## Add cooking step
		for row in c.execute('SELECT max(Zeit) FROM Hopfengaben WHERE SudID = ?', (id,)):
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

		s = Step()
		s.name = "Whirlpool"
		s.order = order
		s.type = 'M'
		s.state = 'I'
		s.temp = 0
		s.timer = 15
		db.session.add(s)
		db.session.commit()
		order +=1
		init()
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
    		file.save(os.path.join('.', 'import.db'))
        	return self.render('admin/imp_result.html')

admin.add_view(StepsAdmin(Step, db.session, name="Steps"))
admin.add_view(KBSelect(name='Recipe List', category='Kleiner Brauhelfer'))
admin.add_view(KBUpload(name='Upload', category='Kleiner Brauhelfer'))
