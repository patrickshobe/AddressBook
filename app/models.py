from app import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    address = db.Column(db.String(250))
    city = db.Column(db.String(120))
    state = db.Column(db.String(20))
    zip = db.Column(db.Integer)

    def __repr__(self):
        return '<Address {}>', format(self.address)

