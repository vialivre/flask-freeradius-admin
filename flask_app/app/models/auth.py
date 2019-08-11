from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, index=True)
    description = db.Column(db.Text)

