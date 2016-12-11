from brewapp import app, db
from model import *


from flask_superadmin import Admin, model
admin = Admin(app)
admin.register(Step, session=db.session)
admin.register(RecipeBooks, session=db.session)
admin.register(RecipeBookSteps, session=db.session)
admin.register(Kettle, session=db.session)
admin.register(Hardware, session=db.session)
admin.register(Config, session=db.session)
admin.register(Fermenter, session=db.session)
admin.register(FermenterStep, session=db.session)
admin.register(Hydrometer, session=db.session)
