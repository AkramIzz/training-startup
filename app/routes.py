import os
from app import app , db , moment
from datetime import datetime
from flask import render_template , redirect , flash , url_for , \
    request , abort, send_from_directory
from werkzeug.utils import secure_filename
from app.forms import * 
from flask_login import current_user , login_user , logout_user , login_required
from app.models import *
from werkzeug.urls import url_parse



def get_new_user_data(user_type , form):
    data = {
        "username" : form.username.data.strip() , 
        "email" : form.email.data.strip() , 
        "fullname" : form.fullname.data.strip() , 
        "gender" : form.gender.data , 
        "birthdate" : form.birthdate.data  , 
        "phone" : form.phone.data.strip()  , 
        "password" : form.password.data.strip() , 
        "user_type" : user_type
    }
    new_user = None
    if user_type == "trainee" : 
        data["academic_level"] = form.academic_level.data.strip()
        new_user = Trainee(data)
    elif user_type == "trainer" :
        data["specialization"] = form.specialization.data.strip()
        new_user = Trainer(data)
    elif user_type == "training_center" : 
        data["center_name"] = form.center_name.data.strip() 
        data["specialization"] = form.specialization.data.strip() 
        data["address"] = form.address.data.strip() 
        new_user = TrainingCenter(data)
    elif user_type == "lecture_room" :
        data["room_name"] = form.room_name.data.strip() 
        data["address"] = form.address.data.strip()
        data["fees"] = form.fees.data
        data["chairs"] = form.chairs.data
        new_user = LectureRoom(data) 
        
    return new_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register/' , methods=['GET' , 'POST'])
def register():
    arr = [
        {"label" : "Trainee" , "class" : "red_gradient" , 
        "href":url_for('register_type',user_type='trainee')} ,

        {"label" : "Trainer" , "class" : "blue_gradient" , 
        "href":url_for('register_type',user_type='trainer')} ,

        {"label" : "Training Center" , "class" : "green_gradient" , 
        "href":url_for('register_type',user_type='training_center')} ,

        {"label" : "Lecture Room" , "class" : "violent_gradient" , 
        "href":url_for('register_type',user_type='lecture_room')} 
    ]
    return render_template('select_type_register.html',arr=arr)


@app.route('/register/<user_type>' , methods=['GET' , 'POST'])
def register_type(user_type):
    dict_ = {"trainee":TraineeForm() , 
            "trainer":TrainerForm() , 
            "training_center":TrainingCenterForm(),
            "lecture_room":LectureRoomForm() }
    if user_type not in dict_ : 
        return "Error"
    form = dict_[user_type]
    if form.validate_on_submit():
        new_user = get_new_user_data(user_type,form)
        db.session.add(new_user)
        db.session.commit() 
        flash ("You Can Now Log in") 
        return redirect(url_for('login'))
    
    return render_template('_form.html',form=form)

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    form.form_name.data = "login_form"
    if form.validate_on_submit():
        username =  form.username.data
        user = Trainee.query.filter_by(username=username).first() or \
               Trainer.query.filter_by(username=username).first() or \
               TrainingCenter.query.filter_by(username=username).first() or \
               LectureRoom.query.filter_by(username=username).first() 

        if user is None or not user.check_password(form.password.data) :
            flash("Username  incorrect")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('_form.html',form=form)

@app.route('/user/<username>')
def user(username):
    user = user = Trainee.query.filter_by(username=username).first() or \
               Trainer.query.filter_by(username=username).first() or \
               TrainingCenter.query.filter_by(username=username).first() or \
               LectureRoom.query.filter_by(username=username).first() 
    if user == "None":
        abort(404)
    
    return render_template('user.html',user=user) 

@app.route('/user/upload', methods=['GET' , 'POST'])
@login_required
def upload():
    form = UploadMedia()
    form.form_name = "media_form"
    if form.validate_on_submit():
        media = request.files.getlist('media')
        if not media:
            return render_template('_form.html', form=form)
        save_files(media)
        flash('upload sucessful')

    return render_template('_form.html' , form=form)

def save_files(files):
    for f in files:
        if not is_allowed_extension(f.filename):
            continue
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def is_allowed_extension(name):
    if '.' in name and name.rsplit('.')[1] in app.config['ALLOWED_EXTENSIONS']:
        return True
    return False

@app.route('/uploads/<media>')
def uploads(media):
    return send_from_directory(app.config['UPLOAD_FOLDER'], media)

@app.route('/test')
def test():
    return "AS"
