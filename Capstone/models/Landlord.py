from User import User
from Capstone import db

class Landlord(User):
    units = db.relationship('Unit', backref='landlord', lazy=True)
    payments = db.relationship('Payment', backref='landlord', lazy=True)