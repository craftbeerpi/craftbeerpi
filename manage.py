#!/usr/bin/env python

from flask.ext.script import Manager
from brewapp.base.model import *
from brewapp import app, db
from flask import Flask, abort, redirect, url_for, render_template

manager = Manager(app)


@manager.command
def dump():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
        
    for line in sorted(output):
        print line


if __name__ == "__main__":
    manager.run()
