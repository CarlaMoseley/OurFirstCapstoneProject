from BaseModel import BaseModel
from Capstone import db

class Payment(BaseModel):
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    amount = db.Column(db.Double, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=True)
    date = db.Column(db.Date, nullable=False, default=db.func.current_timestamp().date())