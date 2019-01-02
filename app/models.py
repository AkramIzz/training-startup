from datetime import datetime
from werkzeug import generate_password_hash  , check_password_hash
from app import db  , app
from flask_login import UserMixin
from app import login 
from hashlib import md5
from sqlalchemy.event import listens_for

import sys

def _print(s):
    print("#"*20+"\n" +
             str(s) + "\n" +
         "#"*20, file=sys.stdout)


@login.user_loader 
def load_user(data):
    # data{ "username" : username , "user_type" : user_type }

    _print(data)
    user_name = data["username"] 
    user_type = data["user_type"] 

    users = {
        "trainee" : Trainee.query.filter_by(username=user_name).first() ,
        "trainer" : Trainer.query.filter_by(username=user_name).first() ,
        "training_center" : TrainingCenter.query.filter_by(username=user_name).first() ,
        "lecture_room" : LectureRoom.query.filter_by(username=user_name).first() 
    }
    user = None 
    user = users[user_type]

    return user

class User(UserMixin ,db.Model):

    def __init__(self,data):
        self.username = data["username"] 
        self.user_type = data["user_type"]
        self.email = data["email"] 
        self.fullname = data["fullname"] 
        self.gender = ("True" == data["gender"] )
        self.birthdate = data["birthdate"] 
        self.phone = data["phone"]
        self.set_password(data["password"])
    
    __abstract__ = True 
    
    id = db.Column(db.Integer , primary_key=True)

    username = db.Column(db.String(64) ,index=True,unique=True)

    email = db.Column(db.String(120) ,index=True,unique=True)

    fullname = db.Column(db.String(120) ,index=True)

    gender = db.Column(db.Boolean,unique=False , default=True)
    # True => Male , False => Female

    activated = db.Column(db.Boolean,unique=False ,
         default=app.config["ACTIVATED_AFTER_REGISTER"])

    phone = db.Column(db.String )

    birthdate = db.Column(db.Date) 
    
    password_hash = db.Column(db.String(128))

    user_type = db.Column(db.String() , default="training_center")

    
    
    def get_id(self):
        return {"username":self.username , "user_type": self.user_type }

    def get_user_type(self):
        return "Trainer"

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)

    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    def __repr__ (self):
        return '<User> {}'.format(self.username)

class Trainee(User):
    def __init__(self,data):
        super(Trainee,self).__init__(data)
        self.academic_level = data["academic_level"]

    def get_id(self):
        return {"username":self.username , "user_type": self.user_type}
    
    def get_user_type(self):
        return "Trainee"
    
    academic_level = db.Column(db.String)


class Trainer(User):
    def __init__(self,data):
        super(Trainer,self).__init__(data)
        self.specializtion = data["specialization"]
    def get_user_type(self):
        return "Trainer"
    specialization = db.Column(db.String(180))


class TrainingCenter(User):
    def __init__(self,data):
        super(TrainingCenter,self).__init__(data)
        self.center_name = data["center_name"]
        self.specialization = data["specialization"]
        self.address = data["address"] 
    
    def get_user_type(self):
        return "Training Center"
    center_name = db.Column(db.String(180))
    specialization = db.Column(db.String(180))
    address = db.Column(db.String(180))

class LectureRoom(User):
    def __init__(self,data):
        super(LectureRoom,self).__init__(data)
        self.room_name = data["room_name"]
        self.address = data["address"] 
        self.fees = data["fees"] 
        self.chairs = data["chairs"] 
    
    def get_user_type(self):
        return "Lecture Room"
    room_name = db.Column(db.String(180))
    address =  db.Column(db.String(180))
    fees = db.Column(db.Integer())
    chairs = db.Column(db.Integer())

