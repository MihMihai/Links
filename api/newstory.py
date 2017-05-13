#!/usr/bin/python3

from flask import Blueprint, Response, request
from db_handler import DbHandler
from error_response import ErrorResponse

import token_encoder
import json
import jwt
import time
import base64

appNewStory = Blueprint('api_newstory',__name__)

@appNewStory.route("/api/new_story",methods=['POST'])
def newStory() :

	response = {}

	#get user authentification

	userToken = request.headers.get('Authorization')
	if userToken == None:
		return ErrorResponse.authorization_required()

	#check user authentification

	key = token_encoder.read_key_from_file()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	#connect to db
	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	#get user id
	query = "SELECT id FROM users WHERE auth_token = '%s'" % (userToken)
	cursor.execute(query)
	userData = cursor.fetchone()


	#chech if token is assigned to user, so if query returned something
	if userData == None :
		response['status'] = "Invalid token"
		response['description'] = "Token is not assigned to any user"
		response['status_code'] = 401
		return Response(json.dumps(response,sort_keys = True), mimetype = 'application/json'),401

	userId = userData[0]

	#get text for story
	storyText = request.form.get('text')

	#trim text
	#textMax = 200
	#storyText = storyText[:textMax]

	#get story image
	storyImage = request.form.get('image')

	#get story status
	storyFeel = request.form.get('feel')


	#check if user had a story posted
	query ="SELECT user_id FROM story WHERE user_id = '%d'" % (userId)
	cursor.execute(query)
	storyPresent = cursor.fetchone()

	add = True
	if ( storyText == None or storyText == "" ) \
	and (storyImage == None or storyImage == "") and (storyFeel == None or storyFeel == "") :
		add = False

	if storyImage != None and storyImage != "":
		if "jpeg" in storyImage:
			type = "jpeg"
		else:
			type = "png"
		try:
			storyImage = storyImage[storyImage.index(",") + 1:]
		except ValueError:
			response["error"] = "Bad format for image"
			response["description"] = "Please provide the image in a base64 format"
			response["status_code"] = 400
			return Response(json.dumps(response, sort_keys = True), mimetype = 'application/json'),200
		with open("/var/www/stories/story" + str(userId) + "." + type,'wb') as f:
			f.write(base64.b64decode(storyImage))

	#get current time
	curdate = time.strftime("%Y-%m-%d %H:%M:%S")
	response['date'] = curdate


#	if storyText == None:
#		storyText = "NULL"
#	if storyFeel == None:
#		storyFeel = "NULL"

	#if no story there
	#insert new story in db
	if storyPresent == None :
		if add == True :
			if storyImage != None:
				query = "INSERT INTO story (user_id, text, feel, image, date) VALUES ('%d', '%s', '%s', '%s', '%s')" \
				% (userId, storyText, storyFeel, "story" + str(userId) + "." + type, curdate)
			else:
				query = "INSERT INTO story (user_id, text, feel, image, date) VALUES ('%d', '%s', '%s', '%s', '%s')" \
				% (userId, storyText, storyFeel, storyImage, curdate)

			cursor.execute(query)
			db.commit()
#else update old story
	else :
		if add == True :
			if storyImage != None:
				query = "UPDATE story SET text = '%s', feel = '%s', image = '%s', date = '%s' WHERE user_id = '%d'" \
				%(storyText, storyFeel, "story" + str(userId) + "." + type, curdate, userId)
			else:
				query = "UPDATE story SET text = '%s', feel = '%s', image = '%s', date = '%s' WHERE user_id = '%d'" \
				%(storyText, storyFeel, storyImage, curdate, userId)

			cursor.execute(query)
			db.commit()
	#return response
	response['status'] = "ok"
	return Response(json.dumps(response, sort_keys=True), mimetype = 'application/json'),200





