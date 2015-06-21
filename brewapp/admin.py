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
from brewapp.model import db, Step, Temperatur, Log
from flask.ext.admin import base

## Standard Admin UI for Database models
class StepAdmin(sqla.ModelView):
	form_columns = ['name', 'temp', 'timer', 'type','state','timer_start','start','end','order']

class TempAdmin(sqla.ModelView):
	form_columns = ['time', 'name1', 'value1']

class LogAdmin(sqla.ModelView):
	form_columns = ['time', 'text', 'type']

## Admin View to select a brew 
class KBSelect(BaseView):
    @expose('/')
    def index(self):
        conn = sqlite3.connect('./myapp/dbimport/import.db')
        c = conn.cursor()
        arr = []
        for row in c.execute('SELECT * FROM Sud'):
        	arr.append(row)
        return self.render('imp.html', x= arr)

    # Import brew from kleiner brauhelfer
    @expose('/select')
    def select(self):
    	## delete current brew
		Step.query.delete()
		db.session.commit()


		id = request.args.get("id")
		conn = sqlite3.connect('./myapp/dbimport/import.db')
		c = conn.cursor()
		order = 0


		for row in c.execute('SELECT EinmaischenTemp FROM Sud WHERE ID = ?', id):
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

		return self.render('imp_result.html')

## View to import database from kleiner brauhelfer
class KBUpload(BaseView):

    @expose('/')
    def index(self):
        return self.render('kb_upload.html')

    @expose('/upload',methods=('POST', ))
    def upload(self):
    	if request.method == 'POST':
    		file = request.files['file']
    		filename = secure_filename(file.filename)
    		file.save(os.path.join('./myapp/dbimport/', 'import.db'))
        	return self.render('imp_result.html')

class Back(BaseView):

    @expose('/')
    def index(self):
        return redirect(url_for('login', next=request.url))


## Register Views	

admin = admin.Admin(name="CraftBeerPI")
admin.add_link(base.MenuLink("Zurueck", url="/"))
admin.add_view(StepAdmin(Step, db.session, name="Schritte"))
admin.add_view(TempAdmin(Temperatur, db.session, name="Temperatur Log"))
admin.add_view(LogAdmin(Log, db.session, name="Brauprotokoll"))
admin.add_view(KBSelect(name='Liste', category='Kleiner Brauhelfer'))
admin.add_view(KBUpload(name='Upload', category='Kleiner Brauhelfer'))

admin.init_app(app)

#path = op.join(op.dirname(__file__), 'dbimport')
#admin.add_view(FileAdmin(path, '/dbimport/', name='Static Files'))