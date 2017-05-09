#!/usr/bin/python3

#@param user_email
#@return story_text, story_date
from flask import Blueprint, Response, request

import json
import jwt
import MySQLdb

appStory = Blueprint("api_story",__name__)

@appStory.route("api/story",methods = ['POST'])
def story():

	response = {}

	#get user authentification 

	userToken = request.headers.get('Authorization')
	if userToken == None:
		response['error'] = "Request does not contain an access token"
		response['description'] =  "Authorization required"
		response['status_code'] = 401
		return Response(json.dumps(response, sort_keys=True), mimetype = 'application/json'),401

	#check user authentification

	f = open('server.conf','r')
	key = f.readline()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		response['error'] = "Invalid Token"
		response['description'] = "Token has expired"
		response['status_code'] = 401
		return Response(json.dumps(response, sort_keys = True), mimetype = 'application/json'), 401
	except jwt.InvalidTokenError:
		response['error'] = "Invalid token"
		response['description'] = "Invalid token"
		response['status_code'] = 401
		return Response(json.dumps(response, sort_keys = True), mimetype = 'application/json'), 401
	
	#get friend email and check it's validity
	friendshipId = request.args.get('friendship_id')
	if friendshipId == None or friendshipId == "":
		response['error'] = "Invalid email"
		response['description'] = "Please provide an email"
		response['status_code'] = 400
	return Response(json.dumps(response, sort_keys = True), mimetype = 'application/json'), 400

	#connect to db
	db = MySQLdb.connect(host = "localhost", user = "root", passwd="QAZxsw1234", db="linksdb")
	cursor = db.cursor()

	#get name of user
	query = "SELECT id FROM users WHERE auth_token = '%s'" % (userToken)
	cursor.execute(query)
	userId = cursor.fetchone()

	#get friend id by excluding user id
	query = "SELECT user_1, user_2 from friendships WHERE id = '%d'" % (friendshipId)
	cursor.execute(query)
	ids = cursor.fetchone()

	if ids[0] == userId[0] :
		friendId = ids[0]
	else :
		friendId = ids[1]

	query = "SELECT text,feel,image,date FROM story WHERE user_id = '%d'" % (friendId)
	cursor.execute(query)
	story = cursor.fetchone()

	#only return story parameters that are not null
	text = story[0]
	feel = story[1]
	image = story[2]
	date = story[3]

	if  text != None and text != "" : 
		response['text'] = text
	if feel != None and feel != "" : 
		response['feel'] = feel
	if image != None and image != "" : 
		response['image'] = image

	response['date'] = date

	return Response(json.dumps(response,sort_keys = True),mimetype = 'application/json'), 200











	# get id for friendEmail
	# check if friend id appeas in friendship of user and active

	#if yes



