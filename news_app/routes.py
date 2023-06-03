import os, secrets
from flask import render_template,url_for, redirect, request, flash
from news_app import app, db
from news_app.models import User, Post,Comment, require_writer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from datetime import datetime

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/Register')
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('regiform.html')


@app.route('/Create_User', methods = ['POST', 'GET'] )
def register():
    if request.method == 'POST' :
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return render_template('loginform.html')
    else :
        return render_template('home.html')


@app.route('/Log_in')
def login_form():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('loginform.html')



@app.route('/login', methods = ['POST'])
def login():
    user = User.query.filter_by(email=request.form["email"]).first()
    if user and check_password_hash(user.password, request.form["password"]):
        login_user(user)
        return render_template('welcome.html', name = user.username)

    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(file):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pictures', picture_fn)
    file.save(picture_path)
    return picture_fn




@app.route("/post/new")
@login_required
@require_writer()
def new_post():
    return render_template("new_post.html")


@app.route("/post/create", methods = ['POST', 'GET'])
@login_required
@require_writer()
def create_post():
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        picture = save_picture(request.files["post_picture"])
        post = Post(title=title, post_picture=picture, content=content, author = current_user)
        db.session.add(post)
        db.session.commit()
        return render_template("home.html")




@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/create_comment/<int:post_id>", methods = ['POST'])
@login_required
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form["content"]
    comment = Comment(content = content, commenter =current_user, post_id = post_id)
    db.session.add(comment)
    db.session.commit()
    return render_template('post.html', post=post)