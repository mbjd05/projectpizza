# Models are classes that translate to database tables
# Each class is a table and each attribute is a column
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(1000))