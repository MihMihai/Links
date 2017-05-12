#!/usr/bin/python3

from flask import Blueprint, Response, request
from db_handler import DbHandler
from error_response import ErrorResponse
import json
import jwt

appFriends = Blueprint('api_friends',__name__)


@appFriends.route("/api/friends", methods = ['GET'])
def friends():

	response = {}

	db = DbHandler.get_instance().get_connection()

	#get authorization token for user, used to prevent spamming or unwanted access
	user1Token = request.headers.get("Authorization")

	if user1Token == None:
		return ErrorResponse.authorization_required()

	#get key to code/decode the token
	f = open('server.conf','r')
	key = f.readline()

	#what is coding dictionary user1Acc
	try:
		user1Acc = jwt.decode(user1Token,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	query = "SELECT id FROM users WHERE auth_token ='%s' " % (user1Token)
	cursor = db.cursor()
	cursor.execute(query)

	user1Id = cursor.fetchone()

	if user1Id == None:
		return ErrorResponse.authorization_required()

	#get current user from db
	user1Id = user1Id[0]
	#user1Db[0] = userId

	queryFriends = "SELECT id, user_1, user_2 FROM friendships WHERE (user_1 = '%s' OR user_2 = '%s') AND status = 1 " % (user1Id,user1Id) 
	cursor.execute(queryFriends)
	friendData = cursor.fetchall()


	#check if user has friends
	if cursor.rowcount == 0:
		response["status"] = 'ok'
		response["total"] = 0
		response["friends"] = []
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

	#store friend ids in array as we find them in db data
	#array of tuples (fid, id)
	friendsId = {}

	#need to check in friendData which of user 1 and 2 is the friend
	#row[0] -friendshipid, row[1] -u1, row[2] - u2
	for row in friendData:
		if row[1] != user1Id:
			friendsId[str(row[0])] = row[1]
		else:
			friendsId[str(row[0])] = row[2]



	#do the BIG query
	query = """SELECT f.id, u.name, u.email, u.avatar, u.auth_token
		 FROM  users u JOIN friendships f
		 ON ( (u.id = f.user_1 AND f.user_2 = '%s') OR (u.id = f.user_2 AND f.user_1 = '%s') AND status = 1)
 	WHERE """ % (user1Id,user1Id)
	i = 1
	for fid in friendsId:
		if i == 1:
			i = 0
			query += "u.id = '%s' " % (friendsId[fid])
		else:
			query += "or u.id = '%s' " % (friendsId[fid])


	cursor.execute(query)
	friendsDb = cursor.fetchall()

	#debugging purposes
	#return Response(json.dumps(friendsDb,sort_keys=True),mimetype="application/json")

	friends = []
	#get friends using friend ids

	#data[0] - fid, data[1] - name, data[2] - email
	for data in friendsDb:
		friend = {}
		friend["friendship_id"] = str(data[0])
		friend["name"] = data[1]
		friend["email"] = data[2]
		if data[3] != None:
			avatarBase64 = str(data[3])
			if avatarBase64[0] == 'b':
				avatarBase64 = avatarBase64[1:]
			if avatarBase64[0] == "'":
				avatarBase64 = avatarBase64[1:]
				avatarBase64 = avatarBase64[:len(avatarBase64)-1]
			friend["avatar"] = avatarBase64
		if data[4] != None:
			friend["online"] = 1
		else:
			friend["online"] = 0
		friends.append(friend)

	response["status"] = 'ok'
	response["friends"] = friends
	response["total"] = len(friends)

	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

