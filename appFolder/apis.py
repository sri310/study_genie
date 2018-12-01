import json

from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime
from appFolder import app,db
from appFolder.forms import LoginForm, RegistrationForm, CreatePostForm
from appFolder.models import User,Posts,Activites
from flask_login import login_user, current_user, logout_user, login_required

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

@app.route("/testapi", methods = ['GET'])
def testapi():
    return "hello"

@app.route("/createPost_api/<userid>", methods = ['POST'])
def createPost_api(userid):
    parsed = json.loads(request.json)

    post = Posts(user_id=userid, subject=parsed["subject"], content=parsed["content"], title=parsed["title"], upvote=0,
                 downvote=0)

    db.session.add(post)
    db.session.commit()

    activity = Activites(user_id=userid, post_id=post.id, type="create", timestamp=datetime.now(),
                         content=parsed["subject"])
    db.session.add(activity)
    db.session.commit()

    parsed["post_id"] = post.id
    parsed["activites"] = json.dumps([])
    response = es.index(index="posts", body=parsed, doc_type="posts")
    # print (response)

    return "post created"

@app.route("/updatePost_api/<userid>", methods = ['POST'])
def updatePost_api(userid):
    parsed = json.loads(request.json)
    print(parsed["postid"])
    print(parsed["content"])
    post = Posts.query.filter_by(id=parsed["postid"]).first()
    post.content = parsed["content"]
    activity = Activites(user_id=userid, post_id=parsed["postid"], type="update", timestamp=datetime.now(),
                         content=post.subject)
    db.session.add(activity)
    db.session.commit()

    return "updated"

@app.route("/deletePost_api", methods = ['POST'])
def deletePost_api():
    parsed = json.loads(request.json)
    print(parsed)
    post = Posts.query.filter_by(id=parsed["id"])

    activity = Activites(user_id=parsed["userid"], post_id=parsed["id"], type="delete", timestamp=datetime.now(),
                         content=post.subject)
    Posts.query.filter_by(id=parsed["id"]).delete()
    db.session.add(activity)
    db.session.commit()
    return "deleted"


@app.route("/vote_api", methods = ['POST'])
def vote_api():
    parsed = json.loads(request.json)
    result = 0
    if (parsed["activity"] == 'upvote'):
        post = Posts.query.filter_by(id=parsed["postid"]).first()
        post.upvote += 1
        result = post.upvote
        activity = Activites(user_id=parsed["userid"], post_id=parsed["postid"], type="upvote", timestamp=datetime.now(),
                             content=post.subject)
        db.session.add(activity)
        db.session.commit()
    else:
        if (parsed["activity"] == 'downvote'):
            post = Posts.query.filter_by(id=parsed["postid"]).first()
            post.downvote += 1
            result = post.downvote
            activity = Activites(user_id=parsed["userid"], post_id=parsed["id"], type="downvote",
                                 timestamp=datetime.now(), content=post.subject)
            db.session.add(activity)
            db.session.commit()
    return str(result)


@app.route("/read_api", methods = ['POST'])
def read_api():
    parsed = request.json
    print(parsed)
    post = Posts.query.filter_by(id=parsed["postid"])
    activity = Activites(user_id=parsed["user_id"], post_id=parsed["postid"], type="read",
                         timestamp=datetime.now(), content=post.subject)
    db.session.add(activity)
    db.session.commit()
    return "read"


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


@app.route("/recommendations/<userid>/myPosts", methods=['GET'])
def myPosts(userid):
   posts = []
   results = Posts.query.filter_by(user_id=userid)
   for result in results:
       print(result)
       post = {
           "id": result.id ,
           'title': result.title,
           "subject":result.subject,
           "content": result.content,
           "upvote": result.upvote,
           "downvote": result.downvote
       }
       posts.append(post)

   return jsonify(posts)


@app.route("/search", methods=['GET'])
def search_api():
    parsed = json.loads(request.json)
    searchdata = parsed["search"]
    search_object = {
        "query": {
            "match": {
                "content": searchdata
            }
        }
    }

    response = es.search(index = "posts", body = search_object)
    posts = [res["_source"] for res in response["hits"]["hits"]]
    activity = Activites(user_id=parsed["userid"], post_id="0", type="search", timestamp=datetime.now(),
                         content=searchdata)
    db.session.add(activity)
    db.session.commit()

    return jsonify(posts)


@app.route("/subject_filter/<subject>", methods=['GET','POST'])
def subjectfilter_api(subject):
    posts = []
    results = Posts.query.filter_by(subject=subject)
    for result in results:
        print(result)
        post = {
            "id": result.id,
            'title': result.title,
            "subject": result.subject,
            "content": result.content,
            "upvote": result.upvote,
            "downvote": result.downvote
        }
        posts.append(post)

    return jsonify(posts)


@app.route("/progressbarData/<userid>", methods=["GET"])
def progressbarData(userid):
    sub1={}
    sub1["name"]="Adaptive_Web"
    sub1["value"]=Activites.query.filter_by(content="Adaptive_Web",type="read",user_id=userid).distinct(Activites.post_id).count()

    sub2 = {}
    sub2["name"] = "Java"
    sub2["value"] = Activites.query.filter_by(content="Java", type="read",user_id=userid).distinct(Activites.post_id).count()

    sub3 = {}
    sub3["name"] = "Database_Systems"
    sub3["value"] = Activites.query.filter_by(content="Database_Systems", type="read",user_id=userid).distinct(Activites.post_id).count()

    data = [sub1, sub2, sub3]
    return jsonify(data)

@app.route("/pieChartData/<userid>", methods=["GET"])
def pieChartData(userid):
    sub1 = {}
    sub1["name"] = "Adaptive_Web"
    sub1["value"] = Activites.query.filter_by(content="Adaptive_Web", user_id=userid).count()

    sub2 = {}
    sub2["name"] = "Java"
    sub2["value"] = Activites.query.filter_by(content="Java", user_id=userid).count()

    sub3 = {}
    sub3["name"] = "Database_Systems"
    sub3["value"] = Activites.query.filter_by(content="Database_Systems", user_id=userid).count()

    data = [sub1, sub2, sub3]
    return jsonify(data)

@app.route("/userStatistics/<userid>", methods=["GET"])
def userStatistics(userid):
    data={}
    data["Posts Written"] = Activites.query.filter_by(user_id=userid,type="create").count()
    data["Posts Read"] = Activites.query.filter_by(user_id=userid,type="read").count()
    data["Upvotes Given"] = Activites.query.filter_by(user_id=userid,type="upvote").count()
    data["Downvotes Given"] = Activites.query.filter_by(user_id=userid,type="downvote").count()
    data["Upvotes Received"] = "2"
    data["Downvotes Received"] = "2"

    return jsonify(data)


@app.route("/lineChart/<userid>", methods=["GET"])
def lineChart(userid):
    data = [["2000-06-05", 116], ["2000-06-06", 129], ["2000-06-07", 135], ["2000-06-08", 86], ["2000-06-09", 73],
            ["2000-06-10", 85], ["2000-06-11", 73], ["2000-06-12", 68], ["2000-06-13", 92], ["2000-06-14", 130],
            ["2000-06-15", 245], ["2000-06-16", 139], ["2000-06-17", 115], ["2000-06-18", 111], ["2000-06-19", 309],
            ["2000-06-20", 206], ["2000-06-21", 137], ["2000-06-22", 128], ["2000-06-23", 85], ["2000-06-24", 94],
            ["2000-06-25", 71], ["2000-06-26", 106], ["2000-06-27", 84], ["2000-06-28", 93], ["2000-06-29", 85],
            ["2000-06-30", 73], ["2000-07-01", 83], ["2000-07-02", 125], ["2000-07-03", 107], ["2000-07-04", 82],
            ["2000-07-05", 44], ["2000-07-06", 72], ["2000-07-07", 106], ["2000-07-08", 107], ["2000-07-09", 66],
            ["2000-07-10", 91], ["2000-07-11", 92], ["2000-07-12", 113], ["2000-07-13", 107], ["2000-07-14", 131],
            ["2000-07-15", 111], ["2000-07-16", 64], ["2000-07-17", 69], ["2000-07-18", 88], ["2000-07-19", 77],
            ["2000-07-20", 83], ["2000-07-21", 111], ["2000-07-22", 57], ["2000-07-23", 55], ["2000-07-24", 60]];

    return jsonify(data)


