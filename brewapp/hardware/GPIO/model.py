from brewapp import db

class Config2(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    type = db.Column(db.String(50))
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    options = db.Column(db.String(255))

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return self.name
