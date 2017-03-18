#!/usr/bin/python3

from flask import Blueprint, Response, request
import json
import MySQLdb
import time
import jwt

appFriendRequest = Blueprint('api_friendrequest',__name__)

@appFriendRequest.route("/api/friend_request", methods =['POST'])
def friendRequest():

	response = {}

	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")

	#user1 = request.form.get("email1")
	user1Token = request.headers.get("Authorization")

	if user1Token == None:
		response["error"] = "Request does not contain an access token"
		response["description"] = "Authorization required"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401

	f = open('server.conf','r')
	key = f.readline()

	try:
		user1Acc = jwt.decode(user1Token,key)
	except jwt.ExpiredSignatureError:
		response["error"] = "Invalid token"
		response["description"] = "Token has expired"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401
	except jwt.InvalidTokenError:
		response["error"] = "Invalid token"
		response["description"] = "Invalid token"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401

	user2 = request.form.get("email")

	if user2 == None:
		response["error"] = "Invalid email"
		response["description"] = "Please provide an email"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),400

	query = "SELECT id FROM users WHERE auth_token ='%s' " % (user1Token)
	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()
	if data != None:
		uid1 = data[0]
	#else:
	#	response["error"] = "Invalid email"
	#	response["description"] = "Please provide a correct email"
	#	response["status_code"] = 400

	query = "SELECT id FROM users WHERE email ='%s'" %(user2)
	cursor.execute(query)
	data = cursor.fetchone()

	if data != None:
		uid2=data[0]
		query = "SELECT * FROM friendships WHERE (user_1 = '%d' AND user_2 = '%d') OR (user_1 = '%d' AND user_2 = '%d')" %(uid1,uid2,uid2,uid1)
		cursor.execute(query)
		row = cursor.fetchone()
		if row == None:
			status = "ok"
			curdate = time.strftime("%Y-%m-%d")
			query = "INSERT INTO friendships (user_1,user_2,date,status) VALUES('%d','%d',str_to_date('%s','%%Y-%%m-%%d') ,'%d')" % (uid1, uid2,curdate, 0)
			cursor.execute(query)
			db.commit()
			response["status"] = status
		else:
			response["error"] = "Bad request"
			response["description"] = "Request already sent"
			response["status_code"] = 400
	else:
		response["error"] = "Invalid email"
		response["description"] = "Please provide a correct email"
		response["status_code"] = 400

	db.close()
	if "error" in response:
		return Response(json.dumps(response, sort_keys=True),mimetype="application/json"),400
	return Response(json.dumps(response, sort_keys=True),mimetype="application/json")
