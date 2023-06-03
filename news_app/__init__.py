from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY']='9d157b15e9eb831e3963507532b5a0d5'
#Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:test@localhost/mydatabase'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from news_app import routes
from news_app.models import User, Post, Comment

app.app_context().push()
with app.app_context():
    db.create_all()


