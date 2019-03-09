from app import app , db  
from app.models import User ,Trainee , Trainer  , TrainingCenter , LectureRoom , load_user
from app.models import UserMedia


@app.shell_context_processor
def make_shell_context():
    return {'db' : db , 
    'User':User,
     "LectureRoom":LectureRoom,
     "TrainingCenter":TrainingCenter ,
     'Trainer':Trainer, 
     'Trainee':Trainee ,
     'UserMedia': UserMedia,
      "load_user":load_user}

