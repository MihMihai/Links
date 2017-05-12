#!/usr/bin/python3

from flask  import Blueprint, Response, request
from db_handler import DbHandler
from error_response import ErrorResponse

import jwt
import json

appDeleteStory = Blueprint("api_deletestory",__name__)

@appDeleteStory.route('/api/delete_story', methods=['POST'])
def deleteStory() :

	response = {}

	#get user authentification

	userToken = request.headers.get('Authorization')
	if userToken == None:
		return ErrorResponse.authorization_required()

	#check user authentification

	f = open('server.conf','r')
	key = f.readline()

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

	query = "DELETE FROM story WHERE user_id = '%d'" % (userId)
	cursor.execute(query)

	response['status'] = "ok"
	return Response(json.dumps(response,sort_keys = True), mimetype = 'application/json'), 200
