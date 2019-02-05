import os
from app import app , db , moment , babel
from datetime import datetime
from flask import render_template , redirect , flash , url_for , \
    request , abort, send_from_directory, session
from werkzeug.utils import secure_filename
from app.forms import * 
from flask_login import current_user , login_user , logout_user , login_required
from app.models import *
from werkzeug.urls import url_parse
from flask_babel import _ 

from app.managers.search_manager import SearchManager

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
        if user_type == 'trainee':
            session['user'] = new_user.user_id
            return redirect(url_for('choose_interests', user_type=user_type))
        return redirect(url_for('login'))
    
    return render_template('_form.html',form=form)


@app.route('/register/<user_type>/interests', methods=['GET', 'POST'])
def choose_interests(user_type):
    # this ensures that only through registeration the user entered this
    # route
    user_id = session.pop('user', None)
    if user_id is None:
        return redirect('index')

    interests = Tag.query.all()
    interests = [(i.id, i.name) for i in interests]
    form = InterestsForm()
    form.interests_id.choices = interests
    if form.validate_on_submit():
        user = Trainee.query.get(user_id)
        selected = Tag.query.filter(Tag.id.in_(form.interests_id.data))
        user.interests.extend(selected)
        db.session.commit()
        return redirect(url_for('index'))

    # add the user_id to session, because POST and GET requests are
    # processed in the same route
    session['user'] = user_id
    return render_template('_form.html', form=form)


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
    if form.validate_on_submit():

        media = request.files.getlist('media')
        if not media:
            return render_template('user.html',user=user , form=form) 
        

        status = None
        if form.form_name.data == "upload_media":
            status = save_files(media)
        else:
            status = save_files(media,"upload_image")
        msg = _('upload sucessful') if status else _('upload error')
        flash(msg)

        #return redirect(url_for('user',username=username))
    
    return render_template('user.html',user=user , form=form) 

@app.route('/test',methods=['GET','POST'])
def test():
    form = UploadMedia()

    if form.validate_on_submit():
        for field in form : 
            flash("%s : %s" %(field.name, field.data))
            flash("*"*20)
    return render_template('_form.html',form=form)
@app.route('/user/delete/<filename>/')
@app.route('/user/delete/<filename>/<type>')
@login_required
def delete_upload(filename,type="user_media"):

    if type=="user_image":
        os.remove(os.path.join(get_user_uploads_directory(), current_user.image))
        current_user.image = None 
        db.session.commit() 
        return redirect(url_for('user', username=current_user.username))
        
    media = UserMedia.query.filter_by(user=current_user, filename=filename).all()
    for m in media:
        os.remove(os.path.join(get_user_uploads_directory(), m.filename))
        db.session.delete(m)
    db.session.commit()
    return redirect(url_for('user', username=current_user.username))


def save_files(files,type="upload_media"):
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
            if type=="upload_media":
                file_is_video = is_video(filename) 
                db.session.add(UserMedia(user=current_user, filename=filename,filetype=file_is_video))
            else:
                # First delete the old image if there is one
                if current_user.image :
                    os.remove(os.path.join(get_user_uploads_directory(), current_user.image))
                
                # Then save the new image
                current_user.image = filename
            f.save(os.path.join(get_user_uploads_directory(), filename))
    db.session.commit()
    return all_valid


def is_video(name):
    ext = name.rsplit('.')[1].lower()
    if ext in ['3gp', 'avi','mov', 'mp4', 'webm'] :
        return True
    return False

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
        return redirect(url_for('index'))
    return render_template('_form.html',form=form)

@app.route('/suggest',methods=['GET','POST'])
@app.route('/suggest/',methods=['GET','POST'])
@login_required
def suggest():
    form = SuggestionForm() 
    if form.validate_on_submit():
        content = form.content.data.strip() 
        user = current_user 

        db.session.add( Suggestion(user=user , content=content) )
        db.session.commit() 


        flash("Your suggestion have been sent") 
        return redirect(url_for('index'))

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

@app.route('/register/<id>',methods=['GET','POST'])
@app.route('/register/<id>/',methods=['GET','POST'])
@login_required
def registerCourse(id):
    course = Course.query.filter_by(id=int(id)).first_or_404() 
    
    a = Application(user=current_user , course=course) 

    db.session.add(a) 
    db.session.commit() 

    flash("You registration have been added")
    return redirect(url_for('index'))

@app.route('/search')
def search_courses():
    search_manager = SearchManager()

    tags = request.args.get('tag', None)
    keywords = request.args.get('keywords', None)
    duration = request.args.get('duration', None)
    categories = request.args.get('category', None)
    sort_order = request.args.get('sort', None)
    start_date = request.args.get('start_date', None)
    fees = request.args.get('fees', None)
    if categories:
        categories = map(lambda c: c.lower().capitalize(), categories.split('-'))
        search_manager.add_categories_filter(categories)
    if tags:
        tags = map(lambda t: t.lower().capitalize(), tags.split('-'))
        search_manager.add_tags_filter(tags)
    if keywords:
        keywords = map(lambda k: k.lower(), keywords.split('-'))
        search_manager.add_keywords_filter(keywords)
    if duration:
        search_manager.add_duration_filter(duration)
    if sort_order:
        search_manager.sort_by(sort_order)
    if start_date:
        start_date = start_date.split('-')
        start_date = datetime.datetime.strptime(start_date, '%d%m%Y').date()
        search_manager.add_start_date_filter(start_date)
    if fees:
        fees = map(int, fees.split('-'))
        if (len(fees) < 3):
            search_manager.add_fees_filter(*fees)

    courses = search_manager.get_result()
    return render_template('search_page.html', courses=courses)