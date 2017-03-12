#!/usr/bin/python3

from flask import Blueprint, Response, request
import json
import MySQLdb
import time
appFriendRequest = Blueprint('api_friendrequest',__name__)

@appFriendRequest.route("/api/friend_request", methods =['POST'])
def friendRequest():
	
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	
	user1 = request.form.get("email1")
	user2 = request.form.get("email2")
	
	response = {}
	
	query = " SELECT id FROM users WHERE email ='%s' " % (user1)
	status = "not_ok"
	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()
	if data != None:
		uid1 = data[0]
	else:
		reponse["error"] = "Invalid email"
		reponse["status_code"] = 400

	query = "SELECT id FROM users WHERE email ='%s'" %(user2)
	cursor.execute(query)
	data = cursor.fetchone()
	
	if data != None:
		uid2=data[0]
		status = "ok"
		curdate = time.strftime("%Y-%m-%d")
		query = "INSERT INTO friendships (user_1,user_2,date,status) VALUES('%i','%i',str_to_date('%s','%%Y-%%m-%%d') ,'%i')" % (uid1, uid2,curdate, 0)
		cursor.execute(query)
		db.commit()
		response["status"] = status
	else:
		response["error"] = "Invalid email"
		response["status_code"] = 400

	db.close()
	return Response(json.dumps(response, sort_keys=True),mimetype="application/json")
