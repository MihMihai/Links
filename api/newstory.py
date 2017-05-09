#!/usr/bin/python3

# @params : text 
# return status : "ok"

from flask import Blueprint, Response, request

import json
import jwt
import MySQLdb
import time

appNewStory = Blueprint('api_newstory',__name__)

@appNewStory.route("/api/new_story",methods=['POST'])
def newStory() :


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
	
	#connect to db
	db = MySQLdb.connect(host = "localhost", user = "root", passwd="QAZxsw1234", db="linksdb")
	cursor = db.cursor()

	#get user id
	query = "SELECT id FROM users WHERE auth_token = '%s'" % (userToken)
	cursor.execute(query)
	userId = cursor.fetchone()

	#get text for story
	storyText = request.form.get('text')

	#trim text
	#textMax = 200
	#storyText = storyText[:textMax]

	#get story image
	storyImage = request.form.get('image')

	#get story status 
	storyFeel = request.form.get('feel')

	#get current time
	curdate = time.strftime("%Y-%m-%d")

	#check if user had a story posted
	query ="SELECT user_id FROM story WHERE user_id = '%d'" % (userId)
	cursor.execute(query)
	data = cursor.fetchone()

	add = True;
	if (storyText == None or storyText == "" ) and \
	(storyImage == None or storyImage == "") and (storyFeel == None or storyFeel == "") :
		add = False;

	#if no story there
	#insert new story in db
	if data[0] == None :
		if add == True :
			query = "INSERT INTO story (user_id, text, feel, image, date) VALUES ('%d', '%s', '%s') " \
			% (userId[0], storyText, storyFeel, storyImage, curdate)	
			cursor.execute(query)
	#else update old story
	else :
		if add == True : 
			query = "UPDATE story SET text = '%s', text = '%s', feel = '%s', image = '%s', date = '%s' WHERE user_id = '%d'" \
			%(storyText, storyFeel, storyImage, curdate, userId)
			cursor.execute(query)

	#return response
	response['status_code'] = 200
	response['status'] = "ok"
	return Response(json.dumps(response, sort_keys=True), mimetype = 'application/json'),200





