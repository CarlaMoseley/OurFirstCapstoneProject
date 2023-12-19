from Capstone import db
from BaseModel import BaseModel

class User(BaseModel):
    __abstract__ = True
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(65), unique=True, Nullable=False)
    fname = db.Column(db.String(50), Nullable=False)
    lname = db.Column(db.String(50), Nullable=True)
    phone = db.Column(db.String(15), unique=True, Nullable=False)