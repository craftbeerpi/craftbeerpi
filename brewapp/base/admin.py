from admin import *
from brewapp import admin
from flask.ext.admin import base

admin.add_link(base.MenuLink("Back", url="/"))
