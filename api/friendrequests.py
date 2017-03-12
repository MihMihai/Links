#!/usr/bin/python3

from flask import Blueprint,Response,request
import json
import MySQLdb
import jwt

appFriendRequests = Blueprint('api_friendrequests',__name__)

@appFriendRequests.route("/api/friend_requests",methods=['GET'])
def friendRequests():
	response = {}
	
	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234", db="linksdb")
	
	user1Token = request.headers.get("Authorization")
	
	if user1Token == None:
		response["error"] = "Request does not contain an access token"
		response["description"] = "Authorization required"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	
	f = open('server.conf','r')
	key = f.readline()
	
	try:
		userAcc = jwt.decode(user1Token,key)
	except jwt.ExpiredSignatureError:
		response["error"] = "Invalid token"
		response["description"] = "Token has expired"
		response["status_code"] = 401
	except jwt.InvalidTokenError:
		response["error"] = "Invalid token"
		response["description"] = "Invalid token"
		response["status_code"] = 401
	
	query = "SELECT id,user_1 from friendships WHERE user_2='%s'" % (userAcc["sub"])
	
	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	
	fRequests = []
	
	if cursor.rownum() == 0:
		response["status"] = 'ok'
		response["total"] = 0
	
	for row in data:
		fRequests.append(row[0])
	
	query = "SELECT name,email from users WHERE id='%d'" % (fRequests[0][0])
	for (id,user1) in fRequests:
		query = query + " or id='%d'" % (id)
	
	cursor.execute(query)
	data = cursor.fetchall()
	
	users = []
	i = 0
	
	for row in data:
		user = {}
		user["name"] = row[0]
		user["email"] = row[1]
		user["friendship_id"] = fRequests[i][0]
		i++
		users.append(user)
	response["requests"] = users
	response["total"] = cursor.rownum()
	
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	