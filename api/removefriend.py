#!/usr/bin/python3

from flask import Blueprint, Response, request
import json
import MySQLdb
import time
import jwt

appRemoveFriend = Blueprint('api_removefriend',__name__)

@appRemoveFriend.route("/api/remove_friend", methods=['POST'])

def removeFriend():

	response = {}

	db = MySQLdb.connect(host = "localhost", user = "root", passwd="QAZxsw1234", db="linksdb")

	user1Token = request.headers.get("Authorization")
	if user1Token == None:
		response["error"] = "Request does not contain an access token"
		response["description"] =  "Authorization required"
		response["status_code"] = 401
		return Response(json.dumps(response, sort_keys=True), mimetype = "application/json"),401

	f = open('server.conf','r')
	key = f.readline()

	try:
		userAcc = jwt.decode(user1Token,key)
	except jwt.ExpiredSignatureError:
		response["error"] = "Invalid Token"
		response["description"] = "Token has expired"
		response["status_code"] = 401
		return Response(json.dumps(response, sort_keys = True), mimetype = "application/json"), 401
	except jwt.InvalidTokenError:
		response["error"] = "Invalid token"
		response["description"] = "Invalid token"
		response["status_code"] = 401
		return Response(json.dumps(response, sort_keys = True), mimetype = "application/json"), 401

	friendshipID = int( request.form.get("friendship_id"))

	if friendshipID == None:
		response["error"] = "Invalid friendship ID"
		response["description"] = "Please provide an ID"
		response["status_code"] = 400
		return Response(json.dumps(response, sort_keys=True), mimetype="application/json"),400

	uid1= int(userAcc["sub"])

	query = "SELECT * FROM friendships WHERE (user_1 = '%d' OR user_2='%d') AND id='%d' " % (uid1,uid1, friendshipID)
	cursor= db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()
	
	if data != None:
		query = "DELETE FROM friendships WHERE (user_1='%d' OR user_2='%d') AND id= '%d'" %(uid1,uid1,friendshipID)
		cursor.execute(query)
		db.commit()
		response["status"]= "ok"
	else:
		response["error"] = "Invalid friendship ID"
		response["description"] = "Please provide an existing friendship ID"
		response["status_code"] = 400
		return Response(json.dumps(response, sort_keys=True), mimetype="application/json"),400

	db.close()
	return Response(json.dumps(response, sort_keys=True),mimetype="application/json")
