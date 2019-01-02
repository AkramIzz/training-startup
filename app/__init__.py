from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app=app)
migrate = Migrate(app,db)
moment = Moment(app)

login = LoginManager(app)
login.login_view = 'login'


from app import  models  
from app import admin , routes , errors

