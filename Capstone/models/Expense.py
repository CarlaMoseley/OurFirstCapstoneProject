from .BaseModel import BaseModel
from Capstone import db

class Expense(db.Model):
    __tablename__ = 'unit_expenses'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    cost = db.Column(db.Double, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    contractor = db.Column(db.String(100), nullable=True)
    contractor_contact = db.Column(db.String(65))
    date = db.Column(db.Date, nullable=False)