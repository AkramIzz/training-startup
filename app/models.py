from app import app, db, login
from flask_login import UserMixin

from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from hashlib import md5

import sys

def _print(s):
    print("#"*20+"\n" +
             str(s) + "\n" +
         "#"*20, file=sys.stdout)

@login.user_loader
def load_user(id):
    u = User.query.get(id)
    _print({'username': u.username, 'user_type': u.get_type()})
    return User.query.get(id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    fullname = db.Column(db.String(120))
    # True => Male, False => Female
    gender = db.Column(db.Boolean, default=True)
    activated = db.Column(db.Boolean, default=app.config['ACTIVATED_AFTER_REGISTER'])
    phone = db.Column(db.String(16))
    birthdate = db.Column(db.Date)
    password_hash = db.Column(db.String(128))

    language = db.Column(db.Boolean, default=True) # True = english , False : arabic

    trainee = db.relationship('Trainee',cascade="all,delete", back_populates='user', uselist=False)
    trainer = db.relationship('Trainer', cascade="all,delete",back_populates='user', uselist=False)
    training_center = db.relationship('TrainingCenter',cascade="all,delete", back_populates='user', uselist=False)
    lecture_room = db.relationship('LectureRoom',cascade="all,delete", back_populates='user', uselist=False)

    def from_form(form):
        fields = {}
        fields['username'] = form.username.data.strip()
        fields['email'] = form.email.data.strip()
        fields['fullname'] = form.fullname.data.strip()
        fields['gender'] = form.gender.data == "True"
        fields['birthdate'] = form.birthdate.data
        fields['phone'] = form.phone.data.strip()
        u = User(**fields)
        u.set_password(form.password.data)
        return u

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # if you need to know which type it's, use 'u.get_type().__class__'
    def get_type(self):
        return self.trainee or self.trainer or self.training_center or self.lecture_room

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}> {}'.format(self.get_type(), self.username)

class Trainee(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    academic_level = db.Column(db.String(128))
    user = db.relationship('User', back_populates='trainee', uselist=False)

    def from_form(form, user=None):
        if user == None:
            user = User.from_form(form)
        fields = {'user': user}
        fields['academic_level'] = form.academic_level.data.strip()
        return Trainee(**fields)

    def __repr__(self):
        return '<Trainee> {}'.format(self.user_id)

class Trainer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    specialization = db.Column(db.String(180))
    user = db.relationship('User', back_populates='trainer', uselist=False)

    def from_form(form, user=None):
        if user == None:
            user = User.from_form(form)
        fields = {'user': user}
        fields['specialization'] = form.specialization.data.strip()
        return Trainer(**fields)

    def __repr__(self):
        return '<Trainer> {}'.format(self.user_id)

class TrainingCenter(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    center_name = db.Column(db.String(180))
    specialization = db.Column(db.String(180))
    address = db.Column(db.String(180))
    user = db.relationship('User', back_populates='training_center', uselist=False)

    def from_form(form, user=None):
        if user == None:
            user = user.from_form(form)
        fields = {'user': user}
        fields['center_name'] = form.center_name.data.strip()
        fields['specialization'] = form.specialization.strip()
        fields['address'] = form.address.strip()
        return TrainingCenter(**fields)

    def __repr__(self):
        return '<TrainingCenter> {}'.format(self.user_id)

class LectureRoom(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    room_name = db.Column(db.String(180))
    address =  db.Column(db.String(180))
    fees = db.Column(db.Integer)
    chairs = db.Column(db.Integer)
    user = db.relationship('User', back_populates='lecture_room', uselist=False)

    def from_form(form, user=None):
        if user == None:
            user = user.from_form(form)
        fields = {'user': user}
        fields['room_name'] = form.room_name.data.strip()
        fields['address'] = form.address.data.strip()
        fields['fees'] = form.fees.data
        fields['chairs'] = form.chairs.data
        return LectureRoom(**fields)

    def __repr__(self):
        return '<LectureRoom> {}'.format(self.user_id)