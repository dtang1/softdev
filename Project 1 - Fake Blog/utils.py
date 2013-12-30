import pymongo
from bson.objectid import ObjectId

import app
import config as conf


client = pymongo.MongoClient(conf.db)
db = client.SDJJbloginator

users = db.users
posts = db.posts
comments = db.comments

def submitPost(title, body, author, date):
	posts.insert({ "title" : title, "body" : body, "author" : author, "date" : date })

def submitComment(postTitle, body, author, date):
	comments.insert({ "postTitle" : postTitle, "body" : body, "author" : author, "date" : date })

def getPosts():
	return posts.find()

def getPost(postTitle):
	post = posts.find_one({ "title" : postTitle })
	if post is not None:
		post["comments"] = comments.find({ "postTitle" : post["title"] })
	else:
		app.session["error"] = "noPost"
	return post

def deletePost(title, author):
    post = posts.find_one({"title" : title})
    if (author == post['author']):
        posts.remove({"title" : title, "author" :author})
        comments.remove({"postTitle" : title})
        return True
    else:
        return

def deleteComment(title, date, author):
    comment = comments.find_one({"postTitle" : title, "date" : date})
    if (author == comment['author'] ):
        comments.remove({"postTitle" : title, "author" :author, "date" : date})
        return True
    else:
        return
    
def titleAvailable(postTitle):
	if posts.find_one({ "title" : postTitle }) == None:
		return True
	else:
		app.session["error"] = "postFail"
		return False

def getUsers():
	return users.find()

def getUser(username):
	user = users.find_one({ "username" : username })
	if user is not None:
		user["posts"] = posts.find({ "author" : username })
		user["comments"] = comments.find({ "author" : username })
	else:
		app.session["error"] = "noUser"
	return user

def authenticate(username, password):
	user = users.find_one({ "username" : username })
	if user is not None and user["password"] == password:
		return True
	else:
		app.session["error"] = "loginFail"
		return False

def register(username, password, passRetype, security, answer):
	if password != passRetype:
		app.session["error"] = "passMismatch"
	elif users.find_one({"username" : username}) is None:
		users.insert({ "username" : username, "password" : password, "security" : security, "answer" : answer })
		return True
	else:
		app.session["error"] = "userExists"
	return False

def changepass(username, password, newpassword, confirmnewpassword):
    user = users.find_one({'username':username})
    if (password == '' or newpassword == '' or confirmnewpassword == ''):
        app.session["error"] = "emptyField"
        return False
    elif (newpassword != confirmnewpassword or password != user['password']):
        app.session["error"] = "passMismatch"
    else:
        users.update({'username':username},{'$set':{'password':newpassword}})
        return True

def recover(username, security, answer):
    user = users.find_one({'username':username})
    if (username == '' or answer == ''):
        app.session["error"] = "emptyField"
        return False
    elif (security != user['security'] or answer != user['answer']):
        app.session["error"] = "securityMismatch"
        return False
    else:
        return True 
    
def getpass(username):
    user = users.find_one({'username':username})
    return user['password']


def loggedIn():
	if "username" in app.session:
		return True
	else:
		app.session["error"] = "mustLogin"
		return False
