#@param user_email
#@return story_text, story_date

#!user/bin/python3

from flask import Blueprin, Response, request

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
	friendEmail = request.args.get('email')
	if friendEmail == None or friendEmail = "":
		response['error'] = "Invalid email"
		response['description'] = "Please provide an email"
		response['status_code'] = 400
	return Response(json.dumps(response, sort_keys = True), mimetype = 'application/json'), 400

	#connect to db
	db = MySQLdb.connect(host = "localhost", user = "root", passwd="QAZxsw1234", db="linksdb")
	cursor = db.cursor()


	#get id for friendEmail
	#check if friend id appeas in friendship of user and active

	#if yes



