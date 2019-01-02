from app import app , db  
from app.models import User ,Trainee , Trainer  , TrainingCenter , LectureRoom , load_user

'''
def delete_all_posts():
    for p in Post.query.all() : 
        db.session.delete(p)
    db.session.commit()
def p(n):
    return Post.query.get(n)
def u(n):
    return User.query.get(n) 
'''
@app.shell_context_processor
def make_shell_context():
    return {'db' : db , 
    'User':User,
     "LectureRoom":LectureRoom,
     "TrainingCenter":TrainingCenter ,
     'Trainer':Trainer, 
     'Trainee':Trainee ,
      "load_user":load_user}

