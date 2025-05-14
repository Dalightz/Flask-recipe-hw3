import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



basedir = os.path.abspath(os.path.dirname(__file__))



myapp_obj = Flask(__name__)
myapp_obj.config['SECRET_KEY'] = 'supersecretkey'
myapp_obj.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'site.db'))

db = SQLAlchemy(myapp_obj)
login_manager = LoginManager(myapp_obj)
login_manager.login_view = 'login'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


import app.routes
