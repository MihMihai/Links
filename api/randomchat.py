#!/usr/bin/python3
from flask import Blueprint,Response,request
import MySQLdb
import jwt
import json
import random

appRandomChat = Blueprint('api_randomchat',__name__)

@appRandomChat.route('/api/random_chat',methods=['GET'])
def randomChat():
	response = {}

	userToken = request.headers.get("Authorization")

	if userToken == None:
		response["error"] = "Request does not contain an access token"
		response["description"] = "Authorization required"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"), 401

	f = open('server.conf','r')
	key = f.readline()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		response["error"] = "Invalid token"
		response["description"] = "Token has expired"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401
	except jwt.InvalidTokenError:
		response["error"] = "Invalid token"
		response["description"] = "Invalid token"
		response["status_code"] = 401
		return Reponse(json.dumps(response,sort_keys=True),mimetype="application/json"),401

	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234",db="linksdb")

	query = "SELECT id FROM users WHERE id NOT IN (SELECT user_1 FROM friendships WHERE user_2 = '%s' UNION SELECT user_2 FROM friendships WHERE user_1 = '%s')" % (userAcc['sub'],userAcc['sub'])

	cursor = db.cursor()
	cursor.execute(query)
	userIdsRow = cursor.fetchall()

	userIds = []

	for row in userIdsRow:
		userIds.append(row[0])

	userIds.remove(userAcc['sub'])

	randomId = random.choice(userIds)

	randomToken = str(encode_chat_token(randomId))
	randomToken = randomToken[2:]
	randomToken = randomToken[:len(randomToken)-1]

	response["status"] = 'ok'
	response["random_token"] = randomToken

	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

def encode_chat_token(id):
	#this may throw an exception if file doesn't exist
	f = open('server.conf','r')
	key = f.readline()

	try:
		payload = {
			'sub': id
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e
