#!/usr/bin/python3

from flask import Blueprint, Response, request
from db_handler import DbHandler
from error_response import ErrorResponse
import token_encoder
import json
import jwt

appMessages = Blueprint('api_messages',__name__)


@appMessages.route("/api/messages", methods = ['GET'])
def messages():

	response = {}

	db = DbHandler.get_instance().get_connection()
#	db = MySQLdb.connect(host = "localhost",user ="root", passwd = "QAZxsw1234", db="linksdb")

	#get authorization token for user, used to prevent spamming or unwanted access
	userToken = request.headers.get("Authorization")

	if userToken == None:
		return ErrorResponse.authorization_required()

	#get key to code/decode the token
	key = token_encoder.read_key_from_file()

	#what is coding dictionary userAcc
	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()


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
		response["conversations"] = []
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

	#Go get some messages
	conversations = []
	for ID in friendIDs:
		conversation = {}
		query = "SELECT email from users WHERE id = '%d'" % (ID[0])
		cursor.execute(query)
		conversation ['with'] = cursor.fetchone()[0]
		query = "Select user_1, message, time_sent FROM messages WHERE (user_1 = '%d' and user_2 = '%d') or (user_1 = '%d' and user_2 = '%d')" % (uid1,ID[0], ID[0], uid1)
		cursor.execute(query)
		conversation['total'] = cursor.rowcount
		data = cursor.fetchall()
		#data[0] = user_1 data[1]= message data[2] = time_sent
		messages = []
		for entry in data:
			message = {}
			message['message'] = entry[1]
			message['date'] = str( entry[2].strftime("%d-%m-%Y %H:%M:%S"))
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

	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

