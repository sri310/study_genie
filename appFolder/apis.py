import json

from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime
from appFolder import app,db
from appFolder.forms import LoginForm, RegistrationForm, CreatePostForm
from appFolder.models import User,Posts
from flask_login import login_user, current_user, logout_user, login_required

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

@app.route("/testapi", methods = ['GET'])
def testapi():
    return "hello"

@app.route("/createPost_api/<userid>", methods = ['POST'])
def createPost_api(userid):

    parsed = json.loads(request.json)

    post = Posts(user_id = userid,subject=parsed["subject"],content=parsed["content"],title=parsed["title"])

    db.session.add(post)
    db.session.commit()

    parsed["post_id"] = post.id
    parsed["activites"] = json.dumps([])
    response = es.index(index = "posts", body = parsed, doc_type = "posts")
    print (response)

    return "post created"

@app.route("/updatePost_api/<userid>", methods = ['POST'])
def updatePost_api(userid):
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print (parsed["id"])
    print("jyfyurfuirf7iri7r7ir7uir7ui")
    #print(str(parsed))

    #print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"

@app.route("/deletePost_api/<userid>", methods = ['POST'])
def deletePost_api(userid):
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"


@app.route("/vote_api/<userid>", methods = ['POST'])
def vote_api(userid):
    #request.json will be the input received by the api
    #following code prints the json on console
    print(request.json)
    # return incremented/decremented value
    return "1"


@app.route("/read_api/<userid>", methods = ['POST'])
def read_api(userid):
    print(request.json)
    #request.json will be the input received by the api
    #following code prints the json on console
    # parsed = json.loads(request.json)
    # print(json.dumps(parsed, indent=4, sort_keys=True))
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
    post4 = {
        "id": "4",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post2 = {
        "id": "2",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post3 = {
        "id": "3",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    posts = []
    posts.append(post)
    posts.append(post2)
    posts.append(post3)
    posts.append(post4)


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


@app.route("/recommendations/<userid>", methods=['GET'])
def recommendations_user(userid):
    #this api gets recommendations for an user once he is authenticated
    post = {
        "id": "1",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "Authenticated user cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post4 = {
        "id": "4",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "Authenticated user cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post2 = {
        "id": "2",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "Authenticated user cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post3 = {
        "id": "3",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": "Authenticated user cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    posts = []
    posts.append(post)
    posts.append(post2)
    posts.append(post3)
    posts.append(post4)
    return jsonify(posts)


@app.route("/search/<searchdata>", methods=['GET'])
def search_api(searchdata):
    post = {
        "id" : "1",
        'title' : "post_title",
        "subject":"Adaptive web",
        "content": " Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post4 = {
        "id": "4",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": " Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post2 = {
        "id": "2",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": " Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post3 = {
        "id": "3",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": " Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    posts = []
    posts.append(post)
    posts.append(post2)
    posts.append(post3)
    posts.append(post4)


    return jsonify(posts)


@app.route("/subject_filter/<subject>", methods=['GET','POST'])
def subjectfilter_api(subject):
    post = {
        "id" : "1",
        'title' : "post_title",
        "subject":"Adaptive web",
        "content": " Filtered results for a subject. Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post4 = {
        "id": "4",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": " Filtered results for a subject.Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post2 = {
        "id": "2",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": " Filtered results for a subject. Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    post3 = {
        "id": "3",
        'title': "post_title",
        "subject": "Adaptive web",
        "content": " Filtered results for a subject .Search query results This is a test cheat sheet. This is a test cheat sheet. "
                   "This is a test cheat sheet. This is Test cheat sheet. This is a test cheat sheet. This is test cheat sheet.",
        "upvote": "29",
        "downvote": "49"
    }
    posts = []
    posts.append(post)
    posts.append(post2)
    posts.append(post3)
    posts.append(post4)


    return jsonify(posts)


@app.route("/progressbarData/<userid>", methods=["GET"])
def progressbarData(userid):

    sub1 = {
        "name" :"sub1",
        "value" : "75"
    }
    sub2 = {
        "name": "sub2",
        "value": "25"
    }
    sub3 = {
        "name" : "sub3",
        "value" : "50"
    }
    data = [sub1, sub2, sub3]
    return jsonify(data)

@app.route("/pieChartData/<userid>", methods=["GET"])
def pieChartData(userid):

    sub1 = {
        "name" :"sub1",
        "value" : "175"
    }
    sub2 = {
        "name": "sub2",
        "value": "225"
    }
    sub3 = {
        "name" : "sub3",
        "value" : "500"
    }
    sub4 = {
        "name" : "sub4",
         "value" : "300"
    }
    data = [sub1, sub2, sub3,sub4]
    return jsonify(data)

@app.route("/userStatistics/<userid>", methods=["GET"])
def userStatistics(userid):

    data = {
        "Posts Written" : "100",
        "Posts Read" : "200",
        "Upvotes Given" :"400",
        "Upvotes Received" : "200",
        "Downvotes Given": "400",
        "Downvotes Received": "200"
    }

    return jsonify(data)


