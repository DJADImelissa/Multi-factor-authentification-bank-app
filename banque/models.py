from banque import db, login_manager
from banque import bcrypt
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    first_name=db.Column(db.String(length=30), nullable=False)
    last_name=db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    numero=db.Column(db.Integer)
    owned_m = db.Column(db.Integer(), nullable=False, default=8000000)
    code=db.Column(db.Integer,nullable=False,unique=True)
    questions = db.relationship('Question', backref='owned_user', lazy=True)
    transactions=db.relationship('Transaction', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(length=100))
    response = db.Column(db.String(length=50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    montant = db.Column(db.Integer)
    receiver=db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date ,default=datetime.utcnow)
