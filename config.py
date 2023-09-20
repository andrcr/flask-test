import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(): 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE_FILENAME')) \
          if 'DATABASE_FILENAME' in os.environ else ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # good practice would be to get it from an env var from a mounted secret when deployed
    # Flask-WTF uses it for CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret' 