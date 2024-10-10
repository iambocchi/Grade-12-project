from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    userName = db.Column(db.String(150))
    gender = db.Column(db.String(20)) #newest added
    lrn = db.Column(db.Integer, unique=True) #newest added
    phone_number = db.Column(db.Integer, unique=True) #newest added
    darkLight = db.Column(db.String(10), default = 'dark')
    notes = db.relationship('Note')