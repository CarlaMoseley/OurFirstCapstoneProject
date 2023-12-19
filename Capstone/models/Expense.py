from BaseModel import BaseModel
from Capstone import db

class Expense(BaseModel):
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    cost = db.Column(db.Double, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    contractor = db.Column(db.String(100), nullable=True)
    contractor_contact = db.Column(db.String(65))
    date = db.Column(db.Date, nullable=False)