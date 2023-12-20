from Capstone import db
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import BaseQuery

class CustomBaseQuery(BaseQuery):
    pass

class CustomBase:
    query_class = CustomBaseQuery

Base = declarative_base(cls=CustomBase)

class BaseModel(Base):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
