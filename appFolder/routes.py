import json

from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime
from appFolder import app,db
from appFolder.forms import LoginForm, RegistrationForm, CreatePostForm, UpdatePostForm, SearchForm
from appFolder.models import User,Grades
from flask_login import login_user, current_user, logout_user, login_required
from appFolder import  apis
import requests
from time import gmtime, strftime

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True

@app.route("/",  methods=['GET','POST'])
@app.route("/home",  methods=['GET','POST'])
def home():
    form = SearchForm()
    data = requests.get("http://"+request.host+"/recommendations").text
    if form.validate_on_submit():
        print(form.search.data)
        #searchdata = json.loads(form.search.data)
        #print(searchdata)
        data = json.dumps(form.data)

        dataJSON = json.loads(data)
        #print(dataJSON)
        userid = current_user.id
        dataJSON['userid'] = userid
        searchdata = json.dumps(dataJSON)
        url = "http://" + request.host + "/search"
        searchdata = requests.get(url=url,json=searchdata)
        return render_template('home.html', title='home', data=searchdata, form=form, host = request.host)
    if current_user.is_authenticated:
        searchdata = requests.get("http://" + request.host + "/recommendations/" + str(current_user.id)).text
        return render_template('home.html', title='home', data=searchdata, form=form, host=request.host)
    return render_template('home.html',title ='home', data = data, form=form, host=request.host)

@app.route("/<userid>/myPosts")
@login_required
def getMyPosts(userid):
    data = requests.get("http://"+request.host+"/recommendations/"+userid+"/myPosts").text
    return render_template('myPosts.html', title='myPosts', data=data)

@app.route("/subjectSearch/<data>", methods=['GET','POST'])
def subjectSearch(data):
    print(data)
    data = requests.get("http://"+request.host+"/subject_filter/"+data).text
    form = SearchForm()
    return render_template('home.html', title='home', data=data, form=form, host=request.host)

@app.route("/update/<data>", methods=['GET','POST'])
@login_required
def updatePost(data):
    form = UpdatePostForm()
    data = json.loads(data)
    postid = data["id"]
    if form.validate_on_submit():
        print(form.content.data)
        data = json.dumps(form.data)
        dataJSON =json.loads(data)
        dataJSON['postid'] =postid
        data  = json.dumps(dataJSON)
        print(data)
        url = "http://"+request.host+"/updatePost_api/"+str(current_user.id)
        requests.post(url=url,json=data)
        flash(f'Updated post', 'success')
        return redirect(url_for('getMyPosts', userid=current_user.id))
    else:
        form.content.data = data["content"]
    return render_template('updatePost.html', title='updatePost', data=data, form=form)

@app.route("/delete/<postid>")
@login_required
def deletePost(postid):
    url = "http://" + request.host + "/deletePost_api"
    data = postid
    requests.post(url=url, json=data)
    flash(f'Deleted post', 'success')
    return redirect(url_for('getMyPosts', userid=current_user.id))



@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #flash creates a one time alert

        email = User.query.filter_by(email=form.email.data).first()
        user =  User.query.filter_by(username=form.username.data).first()
        if not user and not email:

            user = User(username = form.username.data, email = form.email.data, password = form.password.data,
                        school_year = form.school_year.data, gpa = form.gpa.data)
            db.session.add(user)
            db.session.commit()

            for sub in form.courses.data:
                grade = Grades(user_id=user.id,subject=sub,grade=form.gpa.data)
                db.session.add(grade)
                db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            login_user(user)
            return redirect(url_for('profile',userid=current_user.id))
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
        url = "http://"+request.host+"/createPost_api/"+str(current_user.id)
        requests.post(url=url,json=data)
        flash(f'Post Created', 'success')
        return redirect(url_for('getMyPosts', userid=current_user.id))
    return render_template('createPost.html', title = "create", form = form)

@app.route("/discussions", methods=['GET','POST'])
def discussions():
    form =  CreatePostForm()
    return render_template('discussion.html', title = "Discussions")

@app.route("/addFeed", methods=['GET','POST'])
def addFeed():
    cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    content = request.args.get('feed')
    username = current_user.username
    feed = '''<article class="media content-section"> <img class="rounded-circle article-img" src="static/profile_pics/default.png"> <div class="media-body"> <div class="article-metadata"> <a class="mr-2" href="#">'''+ username +'''</a> <small class="text-muted">'''+ cur_time +'''</small> </div> <p class="article-content">'''+ content +'''</p> </div> </article>'''
    return feed

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
            print(current_user.username)
            return redirect(url_for('profile',userid=current_user.id))
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
    return render_template('profile.html',title='profile', id=userid, host=request.host)






