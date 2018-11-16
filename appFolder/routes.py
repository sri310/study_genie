import json

from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime
from appFolder import app,db
from appFolder.forms import LoginForm, RegistrationForm, CreatePostForm, UpdatePostForm
from appFolder.models import User
from flask_login import login_user, current_user, logout_user, login_required
from appFolder import  apis
import requests

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True

@app.route("/")
@app.route("/home")
def home():
    data = requests.get("http://"+request.host+"/recommendations").text
    return render_template('home.html',title ='home', data = data)

@app.route("/<userid>/myPosts")
@login_required
def getMyPosts(userid):
    data = requests.get("http://"+request.host+"/recommendations/"+userid+"/myPosts").text
    return render_template('myPosts.html', title='myPosts', data=data)

@app.route("/update/<data>", methods=['GET','POST'])
@login_required
def updatePost(data):
    form = UpdatePostForm()
    data = json.loads(data)
    form.content.data = data['content']
    if form.validate_on_submit():
        data = json.dumps(form.data)
        url = "http://"+request.host+"/updatePost_api"
        requests.post(url=url,json=data)
        flash(f'Updated post', 'success')
        return redirect(url_for('getMyPosts', userid=current_user.id))
    return render_template('updatePost.html', title='updatePost', data=data, form=form)

@app.route("/delete/<postid>")
@login_required
def deletePost(postid):
    url = "http://" + request.host + "/deletePost_api"
    data = postid
    requests.post(url=url, json=data)
    flash(f'Deleted post', 'success')
    return redirect(url_for('getMyPosts', userid=current_user.id))


@app.route("/vote/<data>")
@login_required
def voteActivity(data):
    url = "http://" + request.host + "/vote_api"
    data = data
    requests.post(url=url, json=data)
    return redirect(url_for('home'))


@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #flash creates a one time alert

        email = User.query.filter_by(email=form.email.data).first()
        user =  User.query.filter_by(email=form.username.data).first()
        if not user and not email:
            user = User(username = form.username.data, email = form.email.data, password = form.password.data,
                        school_year = form.school_year.data, gpa = form.gpa.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
        else:
            flash(f'Account already exists!','danger')
        return redirect(url_for('login'))
        # return redirect({{url_for('profile', userid = current_user.id)}})
    return render_template('register.html', title = "Register", form = form)

@app.route("/create", methods=['GET','POST'])
def create():
    form =  CreatePostForm()
    if form.validate_on_submit():
        data = json.dumps(form.data)
        url = "http://"+request.host+"/createPost_api"
        requests.post(url=url,json=data)
        print(type(jsonify(form.data)))
    return render_template('createPost.html', title = "create", form = form)

@app.route("/login", methods = ['GET','POST'])
def login():
    session.permanent = True
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username =  form.username.data).first()
        if user and (user.password==form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else :
            flash('Unsucessful Login! Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    user = User.query.filter_by(username=current_user.username).first()
    user.last_login = datetime.now()
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))



@app.route("/profile/<userid>")
@login_required
def profile(userid):
    return render_template('profile.html',title='profile', id=userid)






