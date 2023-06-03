from datetime import datetime
from news_app import db, login_manager
from flask_login import  UserMixin, current_user
from flask import render_template,url_for, redirect
from functools import wraps




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default='viewer')
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    post_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', lazy=True)

    



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


def require_writer():
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            role = current_user.role
            if role != 'writer':
                return redirect('/')
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator