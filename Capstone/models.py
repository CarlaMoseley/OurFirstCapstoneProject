from .db import db
from sqlalchemy import Sequence


class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, Sequence('andrewm_id_increment'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(65), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

class Landlord(User):
    __tablename__ = 'landlord'
    units = db.relationship('Unit', backref='landlord', lazy=True)
    payments = db.relationship('Payment', backref='landlord', lazy=True)

class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, Sequence('andrewm_id_increment'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    unit_number = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    rent = db.Column(db.Float, nullable=True)
    lease_start = db.Column(db.Date, nullable=True)
    rent_due = db.Column(db.Integer, nullable=True)
    tenant_password = db.Column(db.String(10), nullable=True)
    tenants = db.relationship('Tenant', backref='unit', lazy=True)
    payments = db.relationship('Payment', backref='unit', lazy=True)
    expenses = db.relationship('Expense', backref='unit', lazy=True)

class Tenant(User):
    __tablename__ = 'tenant'
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    payments = db.relationship('Payment', backref='tenant', lazy=True)

class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, Sequence('andrewm_id_increment'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    contractor = db.Column(db.String(100), nullable=True)
    contractor_contact = db.Column(db.String(65))
    date = db.Column(db.Date, nullable=False)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, Sequence('andrewm_id_increment'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=True)
    date = db.Column(db.Date, nullable=False, default=db.func.date(db.func.current_timestamp()))