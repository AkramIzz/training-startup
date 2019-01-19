import os
from app import app , db , moment , babel
from datetime import datetime
from flask import render_template , redirect , flash , url_for , \
    request , abort, send_from_directory
from werkzeug.utils import secure_filename
from app.forms import * 
from flask_login import current_user , login_user , logout_user , login_required
from app.models import *
from werkzeug.urls import url_parse
from flask_babel import _ 


classes_strings = [
    _("left") , _("right") , _("en")
]

@babel.localeselector
def get_language():
    lan = {True:"en",False:"ar"}
    if current_user.is_authenticated:
        if (current_user.language != None) :
            return lan[current_user.language] 
    return "en"

def get_new_user_data(user_type, form):
    if user_type == 'trainee':
        return Trainee.from_form(form)
    if user_type == 'trainer':
        return Trainer.from_form(form)
    if user_type == 'training_center':
        return TrainingCenter.from_form(form)
    if user_type == 'lecture_room':
        return LectureRoom.from_form(form)

    return None

# Return Category object to use it in _base.html
@app.context_processor
def get_context():
    return {"Category":Category}

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
        {"label" : _("Trainee") , "class" : "red_gradient" , 
        "href":url_for('register_type',user_type='trainee')} ,

        {"label" : _("Trainer") , "class" : "blue_gradient" , 
        "href":url_for('register_type',user_type='trainer')} ,

        {"label" : _("Training Center") , "class" : "green_gradient" , 
        "href":url_for('register_type',user_type='training_center')} ,

        {"label" : _("Lecture Room") , "class" : "violent_gradient" , 
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
        flash (_("You Can Now Log in"))
        return redirect(url_for('login'))
    
    return render_template('_form.html',form=form)

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    form.form_name.data = "login_form"
    if form.validate_on_submit():
        username =  form.username.data
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(form.password.data) :
            flash(_("Username  incorrect"))
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('_form.html',form=form)

@app.route('/user/<username>', methods=['GET' , 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == "None":
        abort(404)
    
    form = UploadMedia()
    form.form_name = "media_form"
    if form.validate_on_submit():
        media = request.files.getlist('media')
        if not media:
            return render_template('user.html',user=user , form=form) 
        status = save_files(media)
        msg = _('upload sucessful') if status else _('upload error')
        flash(msg)
    
    return render_template('user.html',user=user , form=form) 


@app.route('/user/delete/<filename>')
@login_required
def delete_upload(filename):
    media = UserMedia.query.filter_by(user=current_user, filename=filename).all()
    for m in media:
        os.remove(os.path.join(get_user_uploads_directory(), m.filename))
        db.session.delete(m)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))

def save_files(files):
    all_valid = True 
    os.makedirs(get_user_uploads_directory(), exist_ok=True)
    for f in files:
        if not is_allowed_extension(f.filename):
            msg = f.filename + " is not allowed type"
            flash(msg)
            all_valid = False
    if all_valid:
        for f in files :
            filename = secure_filename(f.filename)[:128] # Maximum allowed filename length
            db.session.add(UserMedia(user=current_user, filename=filename))
            f.save(os.path.join(get_user_uploads_directory(), filename))
    db.session.commit()
    return all_valid

def is_allowed_extension(name):
    if '.' in name and name.rsplit('.')[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        return True
    return False

@app.route('/uploads/<username>/<media>')
def uploads(username, media):
    media_folder = get_user_uploads_directory(username)
    return send_from_directory(media_folder, media)

def get_user_uploads_directory(username=None):
    if username:
        return os.path.join(app.config['UPLOAD_FOLDER'], str(User.query.filter_by(username=username).first().id))
    return os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id)) 

@app.route('/user/<username>/toggle_lang')
def toggle_lang(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user :
        user.language = True if(user.language == None or user.language == False) else False
        db.session.commit() 
    return redirect(url_for('user',username=username))

@app.route('/addCourse',methods=['GET','POST'])
def add_course():
    form = CourseForm()
    
    # Add choices to trainer field form from the database 
    
    if form.validate_on_submit():
        course = Course.from_form(form)
        db.session.add(course)
        db.session.commit()
        
        flash("Your course has been added") 
    return render_template('_form.html',form=form)


@app.route('/<category>/<tag>/')
@app.route('/<category>/<tag>')
def courses(category,tag):
    cat = Category.query.filter_by(name=category).first_or_404()
    tag = Tag.query.filter_by(name=tag).first_or_404() 
    return render_template('courses_page.html',tag=tag)

@app.route('/<category>/<tag>/<id>/')
@app.route('/<category>/<tag>/<id>')
def course(category,tag,id):
    cat = Category.query.filter_by(name=category).first_or_404()
    tag = Tag.query.filter_by(name=tag).first_or_404() 
    course = Course.query.filter_by(id=int(id)).first_or_404() 
    return render_template('course_page.html',c=course)

