from flask_wtf import Form
from wtforms import StringField , FileField ,IntegerField , HiddenField , PasswordField , BooleanField , SubmitField , TextAreaField , RadioField , SelectField
from wtforms.fields.html5 import DateField , TelField
from wtforms.validators import DataRequired , Email , EqualTo , ValidationError , Length , Required 
from flask_wtf.file import FileRequired
from app.models import * 
from flask_babel import lazy_gettext as _l

class UploadMedia(Form):
    form_name = HiddenField(label=_l("media_form"))
    media = FileField(
        'Select Images' , 
        validators=[FileRequired()]
    )
    submit = SubmitField(_l("Upload"))

class PersonForm(Form):
    form_name = HiddenField(label="Form Name")

    username = StringField(label=_l("Username") , validators=[DataRequired()])

    fullname = StringField(label=_l("Fullname") , validators=[DataRequired()])

    gender = RadioField(_l("Gender") ,validators=[Required()], choices=[("True",_l("Male")),('False',_l("Female"))] , 
                        default=True)

    phone = StringField(_l("Phone number") , validators=[DataRequired()])

    email = StringField(label=_l("Email") , validators=[DataRequired() , Email()])
    email2 = StringField(label=_l("Repeat email") ,  validators=[DataRequired() , EqualTo('email')])

    password = PasswordField(label=_l("Password") ,validators=[DataRequired()] )
    password2 = PasswordField(label=_l("Repeat password") ,  validators=[DataRequired() , EqualTo('password')])

    birthdate = DateField(label=_l("Birthdate"), validators=[Required()])

    
    def validate_username(self , username):
        username = username.data # The data from username field
        user = User.query.filter_by(username=username).first()
         
        if user is not None :
            raise ValidationError(_l("Please use a different username"))

    def validate_email(self , email):
        email = email.data #  The data from email field
        user =  User.query.filter_by(email=email).first() 
        if user is not None :
            raise ValidationError(_l("Please use a different email"))
    

class TraineeForm(PersonForm):
    academic_level = StringField(label=_l("Academic Level") , validators=[DataRequired()])
    submit = SubmitField(_l("Register"))

class TrainerForm(PersonForm):
    specialization = StringField(label=_l("Specialization"),validators=[DataRequired()])
    submit = SubmitField(_l("Register"))


class TrainingCenterForm(PersonForm):
    center_name = StringField(label=_l("Center Name"),validators=[DataRequired()])
    specialization = StringField(label=_l("Specialization"),validators=[DataRequired()])
    address = StringField(label=_l("Address"),validators=[DataRequired()])
    submit = SubmitField(_l("Register"))


class LectureRoomForm(PersonForm):
    room_name = StringField(label=_l("Room Name"),validators=[DataRequired()])
    address = StringField(label=_l("Address"),validators=[DataRequired()])
    fees = IntegerField(label=_l("Fees") , validators=[DataRequired()])
    chairs = IntegerField(label=_l("Chairs") , validators=[DataRequired()])
    
    submit = SubmitField(_l("Register"))


class LoginForm(Form):
    form_name = HiddenField(label="Form Name")

    username = StringField(label=_l("Username") , validators=[DataRequired()])
    password = PasswordField(label=_l("Password") , validators=[DataRequired()])
    #remember_me = BooleanField(label="Remember me")
    submit = SubmitField(label=_l("Sign in") )

class CourseForm(Form):
    form_name = HiddenField(label="Form Name")

    name = StringField(label=_l("Course Name") , validators=[DataRequired()])
    category = StringField(label=_l("Category") , validators=[DataRequired()])

    trainer = StringField(label=_l("Trainer") , validators=[DataRequired()])

    goals = TextAreaField(label=_l("Goals") , validators=[DataRequired()])
    outlines = TextAreaField(label=_l("Outline") , validators=[DataRequired()])
    prerequists = TextAreaField(label=_l("Prerequists") , validators=[DataRequired()])

    target = TextAreaField(label=_l("Target") , validators=[DataRequired()])
    start_date = DateField(label=_l("Start Date") , validators=[DataRequired()])
    duration = StringField(label=_l("Duration") , validators=[DataRequired()])
    time = StringField(label=_l("Time") , validators=[DataRequired()])
    fees = IntegerField(label=_l("Fees") , validators=[DataRequired()])

    submit = SubmitField(_l("Sumbit"))