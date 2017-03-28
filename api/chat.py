#!/usr/bin/python3
from flask_socketio import join_room, leave_room, send
from flask import Blueprint, Response, request
from flask_socketio import SocketIO,emit,send,join_room,leave_room
import json
import MySQLdb
import time
import jwt
from server import app
import eventlet

eventlet.monkey_patch()

#appChat = Blueprint('api_chat',__name__)

socketio = SocketIO(app)

#@socketio.on('connect',namespace='/chat')
#def connect():
#	emit('msg server','Salut')

@socketio.on('msg user',namespace='/chat')
def message(msg):
	dict = json.loads(str(msg))
	to = dict['to']
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")

	if 'random' in dict:
		randomToken = dict['random_token']

		try:
			userAcc = jwt.decode(randomToken)
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

		query = "SELECT chat_token FROM users WHERE id = '%s' " % (userAcc['sub'])
	else:
		query = "SELECT chat_token FROM users WHERE email = '%s' " % (str(to))

	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()
	chatToken = data[0]

	if 'random' in dict:
		dict.pop('random')
		query = "SELECT id FROM users WHERE email = '%s'" % (dict['from'])
		cursor.execute(query)
		fromUserId = cursor.fetchone()
		fromUserToken = str(encode_chat_token(fromUserId[0]))
		fromUserToken = fromUserToken[2:]
		fromUserToken = fromUserToken[:len(fromUserToken)-1]
		dict['from'] = fromUserToken
	else:
		dict.pop('to')

	#del dict['to']
	emit('msg server',json.dumps(dict), room=chatToken)
	#emit('msg server', json.dumps(dict))

@socketio.on('join', namespace='/chat')
def on_join(data):
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	email = data['email']
	query = "SELECT chat_token FROM users WHERE email = '%s' " % (email)
	cursor = db.cursor()
	cursor.execute(query)
	token = cursor.fetchone()
	room = token[0]

	db.close()
	join_room(room)
	emit('msg server',email + ' has entered the room.', room=room)


@socketio.on('leave', namespace='/chat')
def on_leave(data):
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	email = data['email']
	query = "SELECT chat_token FROM users WHERE email = '%s' " % (email)
	cursor = db.cursor()
	cursor.execute(query)
	token = cursor.fetchone()
	room = token[0]

	db.close()
	leave_room(room)
	emit('msg server',email + ' has left the room.', room=room)

@socketio.on('json')
def handle_json(jsonData):
	data = json.loads(jsonData)
	room = data["to"]
	del data["to"]
	send(data,room=room,namespace='/chat')
	#send(data,json=True,room=room,namespace='/chat')

	#send(json, json=True)

	#{
		#to:[the other receiver's username as a string],
		#from:[the person who sent the message as string],
		#message:[the message to be sent as string]
	#}

@socketio.on_error_default
def default_error_handler(e):
	wr = open('socketio-error.log','a')
	wr.write(str(e) + " pare rau\n")
	wr.close()


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
