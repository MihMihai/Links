#!/usr/bin/python3

from flask import Blueprint,Response,request
import json
import jwt
import token_encoder
from db_handler import DbHandler
from error_response import ErrorResponse

appProfile = Blueprint('api_profile',__name__)

@appProfile.route("/api/profile",methods=['GET'])
def friendRequests():
	response = {}

	db = DbHandler.get_instance().get_connection()

	userToken = request.headers.get("Authorization")

	if userToken == None:
		return ErrorResponse.authorization_required()

	key = token_encoder.read_key_from_file()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	query = " SELECT name, email, birthday_date,chat_token,avatar FROM users where id = '%s'" % (userAcc["sub"])

	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()

	if data != None:

		response['name']=data[0]
		response['email']=data[1]
		response['birthday_date']=data[2].strftime('%Y-%m-%d')
		response['chat_token'] = data[3]

		if data[4] != None:
			avatarBase64 = str(data[4])
			if avatarBase64[0] == 'b':
				avatarBase64 = avatarBase64[1:]
			if avatarBase64[0] == "'":
				avatarBase64 = avatarBase64[1:]
				avatarBase64 = avatarBase64[:len(avatarBase64)-1]
			response['avatar'] = avatarBase64
		response['status']='ok'
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	else:
		response['error'] = "Bad token"
		response['description'] = "Something went wrong. Please contact the developers and send them this id: " + userAcc["sub"]
		response['status_code'] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401
