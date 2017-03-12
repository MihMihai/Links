#!/usr/bin/python3
from flask import Blueprint, Response, request
import json
import MySQLdb
import time
import jwt

appAcceptFriend = Blueprint('api_acceptfriend',__name__)

@appAcceptFriend.route("/api/accept_friend", methods =['POST'])
def acceptFriend():

	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")

	response = {}

	auth_token = request.headers.get("Authorization")

	if auth_token == None:
		response["error"] = "Authorization required"
		response["description"] = "Request does not contain an access token"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True), mimetype="application/json")

	f = open('server.conf','r')
	key = f.readline()

	try:
		user = jwt.decode(auth_token,key)
	except jwt.ExpiredSignatureError:
		response["error"] = "Invalid token"
		response["description"] = "Token has expired"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True), mimetype="application/json"),401
	except jwt.InvalidTokenError:
		response["error"] = "Invalid token"
		response["description"] = "Invalid token"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True), mimetype="application/json"),401

	friendshipId = request.form.get("requestID")
	if friendshipId == None:
		response["error"] = "Bad parameters"
		response["description"] = "Please provide a friendship id"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys=True), mimetype="application/json"),400

	requestID = int(friendshipId)
	newDate = time.strftime("%Y-%m-%d")
	cursor = db.cursor()

	queryCheck = "SELECT user_1,user_2 FROM friendships WHERE id='%d'" % (requestID)
	cursor.execute(queryCheck)
	data = cursor.fetchone()

	if data[1] != user["sub"]: #user["sub"] returns the id of the user who performed this action(i.e. wants to accept this request)
		response["error"] = "Invalid friendship id"
		response["description"] = "User doesn't have a friend request with that id"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True), mimetype="application/json"),401

	query = "UPDATE friendships SET status='%d', date=str_to_date('%s','%%Y-%%m-%%d') WHERE id='%d'" % (1,newDate,requestID)
	cursor.execute(query)
	db.commit()
	response["status"]= "ok"

	db.close()
	return Response(json.dumps(response, sort_keys=True), mimetype="application/json")
