#!/usr/bin/python3

from flask import Blueprint,Response,request
from db_handler import DbHandler
from error_response import ErrorResponse
import token_encoder
import json
import jwt

appFriendRequests = Blueprint('api_friendrequests',__name__)

@appFriendRequests.route("/api/friend_requests",methods=['GET'])
def friendRequests():
	response = {}

	db = DbHandler.get_instance().get_connection()

	user1Token = request.headers.get("Authorization")

	if user1Token == None:
		return ErrorResponse.authorization_required()

	key = token_encoder.read_key_from_file()

	try:
		userAcc = jwt.decode(user1Token,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()


	query = "SELECT id,user_1 from friendships WHERE user_2='%s' and status=0" % (userAcc["sub"])

	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchall()

	fRequests = []

	if cursor.rowcount == 0:
		response["status"] = 'ok'
		response["total"] = 0
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

	for row in data:
		fRequests.append(row)

	query = "SELECT name,email,avatar from users WHERE id='%d'" % (fRequests[0][1])
	i = 0
	for (id,uid) in fRequests:
		if i == 0:
			i = 1
			continue
		query = query + (" or id='%d'" % (uid))

	cursor.execute(query)
	data = cursor.fetchall()

	users = []
	i = 0

	for row in data:
		user = {}
		user["name"] = row[0]
		user["email"] = row[1]
		user["friendship_id"] = fRequests[i][0]
		if row[2] != None:
			avatarBase64 = str(row[2])
			if avatarBase64[0] == 'b':
				avatarBase64 = avatarBase64[1:]
			if avatarBase64[0] == "'":
				avatarBase64 = avatarBase64[1:]
				avatarbase64 = avatarBase64[:len(avatarBase64)-1]
			user["avatar"] = avatarBase64
		i+=1
		users.append(user)

	response["status"] = 'ok'
	response["requests"] = users
	response["total"] = cursor.rowcount

	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

