
from app import app , models , db
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup

class UserAdmin(ModelView):

    def gender(view, context, model, name):
        s = "Male" if model.gender else "Female"
        return s
    def activated(view, context, model, name):
        s = "Activated" if model.activated else "Not Activated"
        color = "green" if model.activated else "grey"
        return Markup(
            '<p style="color : %s ">%s</p>' %(color , s)
        )

    column_exclude_list = ["password_hash"]
    column_filters = ["username" , "fullname"]
    can_view_details = True
    page_size = 10 

    column_formatters = {
        'gender': gender , 
        'activated' : activated
    }

class TraineeAdmin(ModelView):
    pass 

class TrainerAdmin(ModelView):
    pass 
class TrainingCenterAdmin(ModelView):
    pass 
class LectureRoomAdmin(ModelView):
    pass 

class CategoryAdmin(ModelView):
    form_excluded_columns = ['tags']

class TagAdmin(ModelView):   
    form_excluded_columns = ['courses','followers'] 

class CourseAdmin(ModelView):
    form_excluded_columns = ['applications']

class MediaAdmin(ModelView):

    def filetype(view, context, model, name):
        s = "Image" if not model.filetype else "Video"
        return s
    
    column_formatters = {
        
        'filetype' : filetype
    }

admin = Admin(app,template_mode='bootstrap3')
admin.add_view(UserAdmin(models.User, db.session))
admin.add_view(TraineeAdmin(models.Trainee , db.session))
admin.add_view(TrainerAdmin(models.Trainer , db.session))
admin.add_view(TrainingCenterAdmin(models.TrainingCenter , db.session))
admin.add_view(LectureRoomAdmin(models.LectureRoom , db.session))
admin.add_view(MediaAdmin(models.UserMedia , db.session))
admin.add_view(CategoryAdmin(models.Category , db.session))
admin.add_view(TagAdmin(models.Tag , db.session))
admin.add_view(CourseAdmin(models.Course , db.session))
admin.add_view(LectureRoomAdmin(models.Suggestion , db.session))
admin.add_view(LectureRoomAdmin(models.Application , db.session))




