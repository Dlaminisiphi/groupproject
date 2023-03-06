from . import db
from flask_login import UserMixin

#database
class User(db.Model, UserMixin):
    id = db.Column(db.Interger, primary_key=True)
    email= db.column(db.String(100), unique=True)
    password=db.column(db.String(150))
    first_name=db.column(db.String(150))
