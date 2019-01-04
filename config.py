import os 
# FLASK_ADMIN_THEMES : cerulean , cosmo
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cosmo'
    POSTS_PER_PAGE = 3
    ACTIVATED_AFTER_REGISTER = False

    UPLOAD_FOLDER = os.path.join(basedir, 'uploads/')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', '3gp', 'avi', 'mp4', 'webm', 'ogg'])
    MAX_CONTENT_LENGTH = 20*1024*1024 # 20MB