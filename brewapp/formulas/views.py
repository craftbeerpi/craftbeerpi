from flask import Blueprint, render_template, jsonify
import json
from brewapp import app, socketio

formulas = Blueprint('formulas', __name__, template_folder='templates', static_folder='static')

@formulas.route('/')
def index():
    return render_template("formulas.html")
