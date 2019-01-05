from flask_wtf import Form
from wtforms import StringField , FileField ,IntegerField , HiddenField , PasswordField , BooleanField , SubmitField , TextAreaField , RadioField , SelectField
from wtforms.fields.html5 import DateField , TelField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError , Length , Required 
from flask_wtf.file import FileRequired
from app.models import * 


class UploadMedia(Form):
    form_name = HiddenField(label="media_form")
    media = FileField(
        'Select Images' , 
        validators=[FileRequired()]
    )
    submit = SubmitField("Upload")

class PersonForm(Form):
    form_name = HiddenField(label="Form Name")

    username = StringField(label="Username" , validators=[DataRequired()])

    fullname = StringField(label="Fullname" , validators=[DataRequired()])

    gender = RadioField("Gender" ,validators=[Required()], choices=[("True","Male"),('False',"Female")] , 
                        default=True)

    phone = StringField("Phone number" , validators=[DataRequired()])

    email = StringField(label="Email" , validators=[DataRequired() , Email()])
    email2 = StringField(label="Repeat email" ,  validators=[DataRequired() , EqualTo('email')])

    password = PasswordField(label="Password" ,validators=[DataRequired()] )
    password2 = PasswordField(label="Repeat password" ,  validators=[DataRequired() , EqualTo('password')])

    birthdate = DateField(label="Birhtday", validators=[Required()])

    
    def validate_username(self , username):
        username = username.data # The data from username field
        user = User.query.filter_by(username=username).first()
         
        if user is not None :
            raise ValidationError("Please use a different username")

    def validate_email(self , email):
        email = email.data #  The data from email field
        user =  User.query.filter_by(email=email).first() 
        if user is not None :
            raise ValidationError("Please use a different email")
    

class TraineeForm(PersonForm):
    academic_level = StringField(label="Academic Level" , validators=[DataRequired()])
    submit = SubmitField("Register")

class TrainerForm(PersonForm):
    specialization = StringField(label="Specialization",validators=[DataRequired()])
    submit = SubmitField("Register")


class TrainingCenterForm(PersonForm):
    center_name = StringField(label="Center Name",validators=[DataRequired()])
    specialization = StringField(label="Specialization",validators=[DataRequired()])
    address = StringField(label="Address",validators=[DataRequired()])
    submit = SubmitField("Register")


class LectureRoomForm(PersonForm):
    room_name = StringField(label="Room Name",validators=[DataRequired()])
    address = StringField(label="Address",validators=[DataRequired()])
    fees = IntegerField(label="Fees" , validators=[DataRequired()])
    chairs = IntegerField(label="Chairs" , validators=[DataRequired()])
    
    submit = SubmitField("Register")


class LoginForm(Form):
    form_name = HiddenField(label="Form Name")

    username = StringField(label="Username" , validators=[DataRequired()])
    password = PasswordField(label="Password" , validators=[DataRequired()])
    #remember_me = BooleanField(label="Remember me")
    submit = SubmitField(label="Sign in" )

