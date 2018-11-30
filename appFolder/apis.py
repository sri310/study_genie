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

    post = Posts(user_id = userid,subject=parsed["subject"],content=parsed["content"],title=parsed["title"],upvote=0,downvote=0)
    activity = Activites(userid = userid,post_id = post.id,type="create",timestamp=datetime.now(),content=parsed["content"])
    db.session.add(post)
    db.session.add(activity)
    db.session.commit()

    parsed["post_id"] = post.id
    parsed["activites"] = json.dumps([])
    response = es.index(index = "posts", body = parsed, doc_type = "posts")
   # print (response)

    return "post created"

@app.route("/updatePost_api", methods = ['POST'])
def updatePost_api():
    #request.json will be the input received by the api
    #following code prints the json on console
    parsed = json.loads(request.json)
    print(parsed["postid"])
    print(parsed["content"])
    #post = Posts.query.filter_by(id=parsed["postid"]).update(dict(content=parsed["content"]))

    #print(post)

    #db.session.commit()
        #print("jyfyurfuirf7iri7r7ir7uir7ui")
    #print(str(parsed))

    #print(json.dumps(parsed, indent=4, sort_keys=True))
    # write code to create a post
    return "posted"

@app.route("/deletePost_api", methods = ['POST'])
def deletePost_api():
    parsed = json.loads(request.json)
    #print(parsed)
    Posts.query.filter_by(id=parsed["id"]).delete()
    activity = Activites(userid=parsed["userid"], post_id=parsed["id"], type="delete", timestamp=datetime.now(),
                         content="NA")
    db.session.add(activity)
    db.session.commit()
    return "deleted"


@app.route("/vote_api", methods = ['POST'])
def vote_api():
    parsed = json.loads(request.json)
    #print(parsed)
    result = 0
    if(parsed["activity"] == 'upvote'):
        post = Posts.query.filter_by(id=parsed["postid"]).first()
        post.upvote+=1
        result = post.upvote
        activity = Activites(userid=parsed["userid"], post_id=parsed["postid"], type="upvote", timestamp=datetime.now(),
                             content="upvote")
        db.session.add(activity)
        db.session.commit()
    else:
        if(parsed["activity"] == 'downvote'):
            post = Posts.query.filter_by(id=parsed["postid"]).first()
            post.downvote+=1
            result = post.downvote
            activity = Activites(userid=parsed["userid"], post_id=parsed["id"], type="downvote", timestamp=datetime.now(),
                                 content="downvote")
            db.session.add(activity)
            db.session.commit()
    return str(result)


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
    #Replace with proper implementation - Abishek bro

    posts = []
    results = Posts.query.filter_by(user_id=1)
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

@app.route("/recommendations/<userid>/myPosts", methods=['GET'])
def myPosts(userid):
   posts = []
   results = Posts.query.filter_by(user_id=userid)
   for result in results:
       #print(result)
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



@app.route("/recommendations/<userid>", methods=['GET'])
def recommendations_user(userid):
    # Replace with proper implementation - Abishek bro
    posts = []
    results = Posts.query.filter_by(user_id=userid)
    for result in results:
       # print(result)
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


@app.route("/search/<searchdata>", methods=['GET'])
def search_api(searchdata):
    search_object = {
        "query": {
            "match": {
                "content": searchdata
            }
        }
    }

    response = es.search(index = "posts", body = search_object)
    posts = [res["_source"] for res in response["hits"]["hits"]]

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

    sub1 = {
        "name" :"Adaptive_Web",
        "value" : "75"
    }
    sub2 = {
        "name": "Java",
        "value": "25"
    }
    sub3 = {
        "name" : "Database_Systems",
        "value" : "50"
    }
    data = [sub1, sub2, sub3]
    return jsonify(data)

@app.route("/pieChartData/<userid>", methods=["GET"])
def pieChartData(userid):

    sub1 = {
        "name" :"Adaptive_Web",
        "value" : "175"
    }
    sub2 = {
        "name": "Java",
        "value": "225"
    }
    sub3 = {
        "name" : "Database_Systems",
        "value" : "500"
    }
    """sub4 = {
        "name" : "sub4",
         "value" : "300"
    }"""
    data = [sub1, sub2, sub3]
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


