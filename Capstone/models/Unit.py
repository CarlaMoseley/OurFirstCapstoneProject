from .BaseModel import BaseModel
from Capstone import db

class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    unit_number = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    rent = db.Column(db.Double, nullable=True)
    lease_start = db.Column(db.Date, nullable=True)
    rent_due = db.Column(db.Integer, nullable=True)
    tenants = db.relationship('Tenant', backref='unit', lazy=True)
    payments = db.relationship('Payment', backref='unit', lazy=True)