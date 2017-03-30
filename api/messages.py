#!/usr/bin/python3

from flask import Blueprint, Response, request
import json
import MySQLdb
import jwt

appMessages = Blueprint('api_messages',__name__)


@appMessages.route("/api/messages", methods = ['GET'])
def messages():

	response = {}

	db = MySQLdb.connect(host = "localhost",user ="root", passwd = "QAZxsw1234", db="linksdb")

	#get authorization token for user, used to prevent spamming or unwanted access
	userToken = request.headers.get("Authorization")

	if userToken == None:
		response["error"] = "Request does not contain an access token"
		response["description"] = "Authorization required"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401

	#get key to code/decode the token
	f = open('server.conf','r')
	key = f.readline()

	#what is coding dictionary userAcc
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
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401


	uid1 = userAcc['sub']	
	# Get all users which have a talk with uid1
	query = "SELECT DISTINCT user_1 FROM messages WHERE user_2 = '%d' UNION SELECT DISTINCT user_2 FROM messages WHERE user_1 = '%d'" % ( uid1, uid1)
	cursor = db.cursor()
	cursor.execute(query)
	
	friendIDs =cursor.fetchall()
	
	#number of discussions
	talks = cursor.rowcount
	
	#check if user has friends
	if talks == 0:
		response["status"] = 'ok'
		response["total"] = 0
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	
	#Go get some messages
	conversations = []
	for ID in friendIDs:
		conversation = {}
		conversation ['with'] = ID
		query = "Select user_1, message, time_sent FROM messages WHERE (user_1 = '%d' and user_2 = '%d') or (user_1 = '%d' and user_2 = '%d')" % (uid1,ID[0], ID[0], uid1)
		cursor.execute(query)
		conversation['total'] = cursor.rowcount
		data = cursor.fetchall()
		#data[0] = user_1 data[1]= message data[2] = time_sent
		messages = []
		for entry in data: 
			message = {}
			message['message'] = entry[1]
			message['date'] =str( entry[2])
			if entry[0] == uid1:
				message['sender'] = 'right'
			else:
				message['sender'] = 'left'
			messages.append(message)
		conversation['messages']=messages
		conversations.append(conversation)
		
	response['status'] = 'ok'
	response['total'] = talks;
	response['conversations'] = conversations
	db.close()
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")	
	
