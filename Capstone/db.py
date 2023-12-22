from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# Create a new SQLAlchemy instance
db = SQLAlchemy(model_class=declarative_base())
