import json

from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime
from appFolder import app,db
from appFolder.forms import LoginForm, RegistrationForm, CreatePostForm
from appFolder.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/testapi", methods = ['GET'])
def testapi():
    return "hello"

@app.route("/createPost_api", methods = ['POST'])
def createPost_api():
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"

@app.route("/updatePost_api", methods = ['POST'])
def updatePost_api():
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"

@app.route("/deletePost_api", methods = ['POST'])
def deletePost_api():
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"


@app.route("/vote_api", methods = ['POST'])
def vote_api():
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"

@app.route("/recommendations", methods=['GET'])
def recommendations():
    post = {
        "id" : "1",
        'title' : "post_title",
        "subject":"Adaptive web",
        "content": "This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    posts = []
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    return jsonify(posts)

@app.route("/recommendations/<userid>/myPosts", methods=['GET'])
def myPosts(userid):
    post = {
        "id" : "1",
        'title' : "post_title",
        "subject":"Adaptive web",
        "content": "This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote" : "29",
        "downvote": "49"
    }
    posts = []
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    posts.append(post)
    return jsonify(posts)