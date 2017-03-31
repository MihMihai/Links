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

	#STORE MESSAGES INTO DB
	query = "SELECT id FROM users WHERE email = '%s'" % (dict['from'])
	cursor.execute(query)
	data = cursor.fetchone()
	uid1 = data[0]
	query = "SELECT id FROM users WHERE email = '%s'" % (to)
	cursor.execute(query)
	data = cursor.fetchone()
	uid2 = data[0]
	query = "INSERT INTO messages (user_1, user_2, message) VALUES('%i','%i','%s')" % (uid1, uid2, str(dict["msg"]))
	cursor.execute(query)
	db.commit()

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


@socketio.on('friend request', namespace='/chat')
def friend_request(data):
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	cursor = db.cursor()

	query = "SELECT id,chat_token FROM users WHERE email ='%s'" %(data['email'])
	cursor.execute(query)
	userId = cursor.fetchone()
	query = "SELECT id,email,name FROM users WHERE chat_token = '%s'" % (data['chat_token'])
	cursor.execute(query)
	user1 = cursor.fetchone()
	uid1 = user1[0]
	email = user1[1]
	name = user1[2]

	if userId != None:
		uid2 = userId[0]
		room = userId[1]
		query = "SELECT * FROM friendships WHERE (user_1 = '%d' AND user_2 = '%d') OR (user_1 = '%d' AND user_2 = '%d')" %(uid1,uid2,uid2,uid1)
		cursor.execute(query)
		row = cursor.fetchone()
		if row == None:
			curdate = time.strftime("%Y-%m-%d")
			query = "INSERT INTO friendships (user_1,user_2,date,status) VALUES('%d','%d',str_to_date('%s','%%Y-%%m-%%d') ,'%d')" % (uid1, uid2,curdate, 0)
			cursor.execute(query)
			db.commit()

			frReqDict = {}
			frReqDict['from'] = email
			frReqDict['name'] = name
			emit('new friend request',json.dumps(frReqDict),room=room)
		else:
			room = data['chat_token']
			emit('bad friend request','Request already sent',room=room)
	else:
		room = data['chat_token']
		emit('bad friend request','Invalid email',room=room)

	db.close()

@socketio.on('response friend request',namespace='/chat')
def accept_friend_request(data):
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	cursor = db.cursor()

	query = "SELECT id,chat_token FROM users WHERE email ='%s'" %(data['email'])
	cursor.execute(query)
	userId = cursor.fetchone()
	query = "SELECT id,email FROM users WHERE chat_token = '%s'" % (data['chat_token'])
	cursor.execute(query)
	user1 = cursor.fetchone()
	uid1 = user1[0]

	if userId != None:
		uid2 = userId[0]
		room = userId[1]
		if data['status'] == 1:
			query = "UPDATE friendships SET status = 1 WHERE (user_1 = '%d' AND user_2 = '%d')" %(uid2,uid1)
		else:
			query = "DELETE from friendships WHERE (user_1 = '%d' AND user_2 = '%d')" % (uid2,uid1)
		cursor.execute(query)
		db.commit()

		frReqDict = {}
		frReqDict['from'] = user1[1]
		frReqDict['status'] = data['status']
		emit('status friend request',json.dumps(frReqDict),room=room)
	else: #not needed
		room = data['chat_token']
		emit('bad friend request','Invalid email',room=room)

	db.close()


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
