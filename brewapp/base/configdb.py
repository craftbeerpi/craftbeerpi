from flask import Blueprint, render_template, jsonify, request
from util import *
from model import *
import time
from brewapp import app, socketio
from views import base

from brewapp import manager


def pre_post(data, **kw):
    if(data["type"] == "json"):
        data["value"] = json.dumps(data["value"])

def post_post(result, **kw):
    if(result["type"] == "json"):
        result["value"] = json.loads(result["value"])

def post_get_many(result, **kw):
    for o in result["objects"]:
        if(o["type"] == "json"):
            o["value"] = json.loads(o["value"])

@brewinit()
def init():
    manager.create_api(Config, methods=['GET', 'POST', 'DELETE', 'PUT'],
    preprocessors={
    'POST':[pre_post],
    'PATCH_SINGLE': [pre_post]},
    postprocessors={
    'POST':[post_post],
    'GET_MANY': [post_get_many],
    'GET_SINGLE':[post_post],
    'PATCH_SINGLE': [post_post]})
