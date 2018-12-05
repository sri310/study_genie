import json
import random
from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime, timedelta
from appFolder import app,db
from appFolder.forms import LoginForm, RegistrationForm, CreatePostForm
from appFolder.models import User,Posts,Activites
from flask_login import login_user, current_user, logout_user, login_required

import sqlite3


from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

def gettimestamp():
    days_to_subtract = random.randint(1,30)
    d = (datetime.today() - timedelta(days=days_to_subtract))
    return d

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
    date = gettimestamp()
    activity = Activites(user_id=userid, post_id=post.id, type="create", timestamp=date,
                         content=parsed["subject"])
    db.session.add(activity)
    db.session.commit()

    obj = json.dumps({})
    obj["content"] = post.content
    obj["post_id"] = post.id

    response = es.index(index="posts", body=obj, doc_type="posts")

    return "post created"

@app.route("/updatePost_api/<userid>", methods = ['POST'])
def updatePost_api(userid):
    parsed = json.loads(request.json)
    post = Posts.query.filter_by(id=parsed["postid"]).first()
    post.content = parsed["content"]
    date = gettimestamp()
    activity = Activites(user_id=userid, post_id=parsed["postid"], type="update", timestamp=date,
                         content=post.subject)
    db.session.add(activity)
    db.session.commit()

    return "updated"

@app.route("/deletePost_api", methods = ['POST'])
def deletePost_api():
    parsed = json.loads(request.json)
    post = Posts.query.filter_by(id=parsed["id"]).first()
    date = gettimestamp()
    activity = Activites(user_id=parsed["userid"], post_id=parsed["id"], type="delete", timestamp=date,
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
        date = gettimestamp()
        activity = Activites(user_id=parsed["userid"], post_id=parsed["postid"], type="upvote", timestamp=date,
                             content=post.subject)
        db.session.add(activity)
        db.session.commit()
    else:
        if (parsed["activity"] == 'downvote'):
            post = Posts.query.filter_by(id=parsed["postid"]).first()
            post.downvote += 1
            result = post.downvote
            date = gettimestamp()
            activity = Activites(user_id=parsed["userid"], post_id=parsed["id"], type="downvote",
                                 timestamp=date, content=post.subject)
            db.session.add(activity)
            db.session.commit()
    return str(result)


@app.route("/read_api", methods = ['POST'])
def read_api():
    parsed = request.json
    post = Posts.query.filter_by(id=parsed["postid"])
    date = gettimestamp()
    activity = Activites(user_id=parsed["user_id"], post_id=parsed["postid"], type="read",
                         timestamp=date, content=post.subject)
    db.session.add(activity)
    db.session.commit()
    return "read"


def getRequiredPosts(query):
	conn = sqlite3.connect("D:\\Arizona State University\\My Github\\study_genie\\appFolder\\site.db")
	cur = conn.cursor()
	cur.execute(query)

	content = ""
	for row in cur.fetchall():
		content = content + row[0] + " "

	search_object = {
		"query": {
			"match": {
				"content": content
			}
		}
	}

	response = es.search(index = "posts", body = search_object)
	posts = [res["_source"]["post_id"] for res in response["hits"]["hits"]]
	posts_str = ""
	for i, post in enumerate(posts):
		posts_str = posts_str + str(post)
		if i != len(posts)-1:
			posts_str += ","
	
	cur.execute("select * from posts where id in ("+posts_str+")")

	posts = []
	for result in cur.fetchall():
		post = {
			"id": result[0] ,
			'title': result[3],
			"subject":result[2],
			"content": result[4],
			"upvote": result[5],
			"downvote": result[6]
		}
	posts.append(post)
	
	cur.close()
	conn.close()

	return jsonify(posts)

@app.route("/recommendations", methods=['GET'])
def recommendations():
	return getRequiredPosts("select content from Posts where Posts.id in (select post_id from (select one.post_id as post_id, two.Searches, three.Reads, four.Upvotes from (select post_id, count(post_id) as Creates from Activites where type=='create' group by post_id) one left join (select post_id, count(post_id) as Searches from Activites where type=='search' group by post_id) two on one.post_id==two.post_id left join (select post_id, count(post_id) as Reads from Activites where type=='read' group by post_id) three on one.post_id==three.post_id left join (select post_id, count(post_id) as Upvotes from Activites where type=='upvote' group by post_id) four on one.post_id==four.post_id order by two.Searches, three.Reads, four.Upvotes)) limit 10")
    


@app.route("/recommendations/<userid>", methods=['GET'])
def recommendations_user(userid):
    #this api gets recommendations for an user once he is authenticated
    return getRequiredPosts("select content from Posts where Posts.id in (select post_id from (select one.post_id as post_id, two.Searches, three.Reads, four.Upvotes from (select post_id, count(post_id) as Creates from Activites where type='create' group by post_id) one left join (select post_id, count(post_id) as Searches from Activites where type=='search' and user_id=="+userid+" group by post_id) two on one.post_id==two.post_id left join (select post_id, count(post_id) as Reads from Activites where type=='read' and user_id=="+userid+" group by post_id) three on one.post_id==three.post_id left join (select post_id, count(post_id) as Upvotes from Activites where type=='upvote' and user_id=="+userid+" group by post_id) four on one.post_id==four.post_id order by two.Searches, three.Reads, four.Upvotes)) limit 10")


@app.route("/recommendations/<userid>/myPosts", methods=['GET'])
def myPosts(userid):
   posts = []
   results = Posts.query.filter_by(user_id=userid)
   for result in results:
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
    posts = [res["_source"]["post_id"] for res in response["hits"]["hits"]]
    conn = sqlite3.connect("D:\\Arizona State University\\My Github\\study_genie\\appFolder\\site.db")
    cur = conn.cursor()

    posts_str = ""
    for i, post in enumerate(posts):
    	posts_str = posts_str + str(post)
    	if i != len(posts)-1:
    		posts_str += ","
    cur.execute("select * from posts where id in ("+posts_str+")")
    
    posts = []
    for result in cur.fetchall():
    	post = {
    	   "id": result[0] ,
           'title': result[3],
           "subject":result[2],
           "content": result[4],
           "upvote": result[5],
           "downvote": result[6]
    	}
    	posts.append(post)

    activity = Activites(user_id=parsed["userid"], post_id="0", type="search", timestamp=gettimestamp(),
                         content=searchdata)
    db.session.add(activity)
    db.session.commit()

    return jsonify(posts)


@app.route("/subject_filter/<subject>", methods=['GET','POST'])
def subjectfilter_api(subject):
    posts = []
    results = Posts.query.filter_by(subject=subject)
    for result in results:
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
    data = []
    list_timestamps = Activites.query.filter_by(user_id=userid).group_by(Activites.timestamp).with_entities(Activites.timestamp)


    for list_ts in list_timestamps:
        for timestamp in list_ts:
            count = Activites.query.filter_by(timestamp=timestamp,user_id=userid).count()
            element= [timestamp.strftime("%Y-%m-%d"),count]
            data.append(element)

    """ data = [["2000-06-05", 116], ["2000-06-06", 129], ["2000-06-07", 135], ["2000-06-08", 86], ["2000-06-09", 73],
            ["2000-06-10", 85], ["2000-06-11", 73], ["2000-06-12", 68], ["2000-06-13", 92], ["2000-06-14", 130],
            ["2000-06-15", 245], ["2000-06-16", 139], ["2000-06-17", 115], ["2000-06-18", 111], ["2000-06-19", 309],
            ["2000-06-20", 206], ["2000-06-21", 137], ["2000-06-22", 128], ["2000-06-23", 85], ["2000-06-24", 94],
            ["2000-06-25", 71], ["2000-06-26", 106], ["2000-06-27", 84], ["2000-06-28", 93], ["2000-06-29", 85],
            ["2000-06-30", 73], ["2000-07-01", 83], ["2000-07-02", 125], ["2000-07-03", 107], ["2000-07-04", 82],
            ["2000-07-05", 44], ["2000-07-06", 72], ["2000-07-07", 106], ["2000-07-08", 107], ["2000-07-09", 66],
            ["2000-07-10", 91], ["2000-07-11", 92], ["2000-07-12", 113], ["2000-07-13", 107], ["2000-07-14", 131],
            ["2000-07-15", 111], ["2000-07-16", 64], ["2000-07-17", 69], ["2000-07-18", 88], ["2000-07-19", 77],
            ["2000-07-20", 83], ["2000-07-21", 111], ["2000-07-22", 57], ["2000-07-23", 55], ["2000-07-24", 60]];
    """


    return jsonify(data)


