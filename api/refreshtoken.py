#!/usr/bin/python3
from flask import Blueprint,request,Response
import MySQLdb
import jwt
import json

appRefresh = Blueprint('api_refreshtoken',__name__)

@appRefresh.route('/api/refresh_token', methods=['GET'])
def refreshToken():
	response = {}
	
	userToken = request.headers.get()
	
	try:
		userAcc = jwt.decode(userToken)
	except jwt.ExpiredSignatureError:
		pass
	except jwt.InvalidTokenError:
		response["error"] = "Invalid token"
		response["description"] = "Invalid token"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401
	
	query = "SELECT id FROM users WHERE auth_token = '%s'" % (userToken)
	
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	
	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()
	if data != None:
		auth_token = str(encode_auth_token(data[0])
		auth_token = auth_token[2:]
		auth_token = auth_token[:len(auth_token)-1]
		response["access_token"] = auth_token
		response["status_ok"] = 'ok'
		db.close()
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	else
		response["error"] = "Invalid token"
		response["description"] = "No user found with the token provided"
		response["status_code"] = 401
		return Response(jsom.dumps(response,sort_keys=True),mimetype="application/json"),401
		

def encode_auth_token(user_id):
	#this may throw an exception if file doesn't exist
	f = open('server.conf','r')
	key = f.readline()

	try:

		payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,seconds=300),
			'iat': datetime.datetime.utcnow(),
			'sub': user_id
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e