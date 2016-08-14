from brewapp import db


class Step(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order = db.Column(db.Integer())
    temp = db.Column(db.Float())
    name = db.Column(db.String(80))
    timer = db.Column(db.Integer())
    type = db.Column(db.String(1))
    state = db.Column(db.String(1))
    timer_start = db.Column(db.DateTime())
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    kettleid = db.Column(db.Integer())

    def __repr__(self):
        return '<Step %r>' % self.name

    def __unicode__(self):
        return self.id


class RecipeBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    steps = db.relationship('RecipeBookSteps', backref='RecipeBooks', lazy='dynamic', cascade="all, delete-orphan")


class RecipeBookSteps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer())
    temp = db.Column(db.Float())
    name = db.Column(db.String(80))
    timer = db.Column(db.Integer())
    type = db.Column(db.String(1))
    kettleid = db.Column(db.Integer())
    receipe_id = db.Column(db.Integer, db.ForeignKey('recipe_books.id'))


class Kettle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sensorid = db.Column(db.String(80))
    heater = db.Column(db.String(10))
    automatic = db.Column(db.String(255))
    agitator = db.Column(db.String(10))
    target_temp = db.Column(db.Integer())
    height = db.Column(db.Integer())
    diameter = db.Column(db.Integer())

    def __repr__(self):
        return '<Kettle %r>' % self.name

    def __unicode__(self):
        return self.id

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    config = db.Column(db.String(256))

    def __repr__(self):
        return '<Hardware %r>' % self.name

    def __unicode__(self):
        return self.id

class Config(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    type = db.Column(db.String(50))
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    options = db.Column(db.String(255))

    def __repr__(self):
        return '<Config %r>' % self.name

    def __unicode__(self):
        return self.name


class Fermenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    brewname = db.Column(db.String(80))
    sensorid = db.Column(db.Integer())
    heaterid = db.Column(db.Integer())
    coolerid = db.Column(db.Integer())
    automatic = db.Column(db.String(255))
    target_temp = db.Column(db.Integer())

    def __repr__(self):
        return '<Fermenter %r>' % self.name

    def __unicode__(self):
        return self.id
'''
class FermenterStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    fermenterid = db.Column(db.Integer())
    temp = db.Column(db.Float())
    hours = db.Column(db.Integer())
    temp = db.Column(db.Integer())
    order = db.Column(db.Integer())
    state = db.Column(db.String(1))
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())

    def __repr__(self):
        return '<FermenterStep %r>' % self.name

    def __unicode__(self):
        return self.id
'''