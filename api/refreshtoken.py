#!/usr/bin/python3
from flask import Blueprint,request,Response
from db_handler import DbHandler
from error_response import ErrorResponse
import jwt
import json
import datetime
import token_encoder

appRefresh = Blueprint('api_refreshtoken',__name__)

@appRefresh.route('/api/refresh_token', methods=['GET'])
def refreshToken():
	response = {}

	userToken = request.headers.get('Authorization')

	if userToken == None:
		return ErrorResponse.authorization_required()

	key = token_encoder.read_key_from_file()

	userAcc = {}

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		pass
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	db = DbHandler.get_instance().get_connection()

	if len(userAcc) == 0:
		query = "SELECT id FROM users WHERE auth_token = '%s'" % (userToken)
		cursor  = db.cursor()
		cursor.execute(query)
		userId = cursor.fetchone()
	else:
		userId = userAcc['sub']

	authToken = str(token_encoder.encode_auth_token(userId))
	authToken = authToken[2:]
	authToken = authToken[:len(authToken)-1]

	query = "UPDATE users SET auth_token = '%s' WHERE auth_token = '%s'" % (authToken,userToken)

	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	#data = cursor.fetchone()

	response["access_token"] = authToken
	response["status"] = 'ok'
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
