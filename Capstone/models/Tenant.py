from User import User
from Capstone import db

class Tenant(User):
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    payments = db.relationship('Payment', backref='tenant', lazy=True)