#!/usr/bin/python3
from flask import Blueprint,request,Response
from db_handler import DbHandler
from error_response import ErrorResponse
import jwt
import json
import datetime

appRefresh = Blueprint('api_refreshtoken',__name__)

@appRefresh.route('/api/refresh_token', methods=['GET'])
def refreshToken():
	response = {}

	userToken = request.headers.get('Authorization')

	if userToken == None:
		return ErrorResponse.authorization_required()

	f = open('server.conf')
	key = f.readline()
	f.close()

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

	authToken = str(encode_auth_token(userId,key))
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


def encode_auth_token(user_id,key):
	#this may throw an exception if file doesn't exist
	#f = open('server.conf','r')
	#key = f.readline()

	try:

		payload = {
			'exp' : datetime.datetime.utcnow() +
			datetime.timedelta(days=0,seconds=300),
			'iat': datetime.datetime.utcnow(),
			'sub': user_id
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e
