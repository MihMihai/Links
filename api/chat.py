#!/usr/bin/python3
from flask_socketio import join_room, leave_room, send
from flask import Blueprint, Response, request
from flask_socketio import SocketIO,emit,send,join_room,leave_room
from db_handler import DbHandler
from User import User
import token_encoder
import json
import time
import jwt
import random
import datetime
from server import app
import eventlet

eventlet.monkey_patch()

#appChat = Blueprint('api_chat',__name__)

socketio = SocketIO(app)

@socketio.on('msg user',namespace='/chat')
def message(msg):
	dict = json.loads(str(msg))
	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	f = open('socketio-error.log','a')
	f.write(str(msg))
	f.close()

	if 'random' in dict:
		randomToken = dict['random_token']

		f = open('server.conf','r')
		key = f.readline()
		f.close()

#		f = open('socketio-error.log','a')
#		f.write('rnd\n')
#		f.close()


		try:
			userAcc = jwt.decode(randomToken,key)
		except jwt.ExpiredSignatureError:
			pass
		except jwt.InvalidTokenError:
			pass

		chatToken = User.get_chat_token_from_id(userAcc['sub'])
	else:
		to = dict['to']
		chatToken = User.get_chat_token_from_email(str(to))


	if 'random' in dict:
		dict.pop('random')
		fromUserId = User.get_id_from_email(dict['from'])
		fromUserToken = str(token_encoder.encode_random_token(fromUserId))
		fromUserToken = fromUserToken[2:]
		fromUserToken = fromUserToken[:len(fromUserToken)-1]
		dict['from'] = fromUserToken
	else:
		dict.pop('to')

		#STORE MESSAGES INTO DB
		uid1 = User.get_id_from_email(dict['from'])
		uid2 = User.get_id_from_email(to)
		query = "INSERT INTO messages (user_1, user_2, message) VALUES('%i','%i','%s')" % (uid1, uid2, str(dict["msg"]))
		cursor.execute(query)
		db.commit()
	dict['date'] = datetime.datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

	emit('msg server',json.dumps(dict), room=chatToken)
	#emit('msg server', json.dumps(dict))

@socketio.on('join', namespace='/chat')
def on_join(data):
	email = data['email']
	room = User.get_chat_token_from_email(email)

	join_room(room)
	emit('msg server',email + ' has entered the room.', room=room)


@socketio.on('leave', namespace='/chat')
def on_leave(data):
	email = data['email']
	room = User.get_chat_token_from_email(email)

	leave_room(room)
	emit('msg server',email + ' has left the room.', room=room)


@socketio.on('friend request', namespace='/chat')
def friend_request(data):
	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	f = open('socketio-error.log','a')
	f.write(str(data))
	f.close()


	if "email" in data:
		userId = User.get_id_and_chat_token_from_email(data['email'])
	else:
		f = open('server.conf','r')
		key = f.readline()
		f.close()

		try:
			userAcc = jwt.decode(data['random_token'],key)
		except jwt.ExpiredSignatureError:
			pass
		except jwt.InvalidTokenError:
			pass

		usrId = userAcc['sub']
		query = "SELECT id,chat_token FROM users WHERE id ='%d'" %(usrId)
		cursor.execute(query)
		userId = cursor.fetchone()

	user1 = User.get_id_email_name_avatar_from_chat_token(data['chat_token'])
	uid1 = user1[0]
	email = user1[1]
	name = user1[2]
	avatar = user1[3]


	if userId != None:
		uid2 = userId[0]

		if uid1 == uid2:
			room = data['chat_token']
			emit('bad friend request','You cannot befriend yourself, sorrrryy..',room=room)
		else:
			room = userId[1]
			query = "SELECT status FROM friendships WHERE (user_1 = '%d' AND user_2 = '%d') OR (user_1 = '%d' AND user_2 = '%d')" %(uid1,uid2,uid2,uid1)
			cursor.execute(query)
			row = cursor.fetchone()
			if row == None:
				curdate = time.strftime("%Y-%m-%d")
				query = "INSERT INTO friendships (user_1,user_2,date,status) VALUES('%d','%d',str_to_date('%s','%%Y-%%m-%%d') ,'%d')" % (uid1, uid2,curdate, 0)
				cursor.execute(query)
				db.commit()


				query = "SELECT id FROM friendships WHERE user_1 ='%d' AND user_2 = '%d'" % (uid1,uid2)
				cursor.execute(query)
				frId = cursor.fetchone()

				frReqDict = {}
				frReqDict['from'] = email
				frReqDict['name'] = name
				frReqDict['friendship_id'] = frId[0]
				if avatar != None:
					avatarBase64 = str(avatar)
					if avatarBase64[0] == 'b':
						avatarBase64 = avatarBase64[1:]
					if avatarBase64[0] == "'":
						avatarBase64 = avatarBase64[1:]
						avatarBase64 = avatarBase64[:len(avatarBase64)-1]
					frReqDict['avatar'] = avatarBase64
				emit('new friend request',json.dumps(frReqDict),room=room)
				emit('friend request sent','Successfully sent the friend request',room=data['chat_token'])
			else:
				room = data['chat_token']
				if row[0] == 0:
					emit('bad friend request','Request already sent',room=room)
				else:
					emit('bad friend request','User is already linked to you',room=room)
	else:
		room = data['chat_token']
		emit('bad friend request','Invalid email',room=room)


@socketio.on('response friend request',namespace='/chat')
def accept_friend_request(data):
	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	userId = User.get_id_and_chat_token_from_email(data['email'])
	user1 = User.get_id_email_name_avatar_from_chat_token(data['chat_token'])
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
		if data['status'] == 1:
			query = "SELECT id FROM friendships WHERE user_1 = '%d' AND user_2 = '%d'" % (uid2,uid1)
			cursor.execute(query)
			frId = cursor.fetchone()
			frReqDict['name'] = user1[2]
			frReqDict['friendship_id'] = frId[0]
			if user1[3] != None:
				avatarBase64 = str(user1[3])
				if avatarBase64[0] == 'b':
					avatarBase64 = avatarBase64[1:]
				if avatarBase64[0] == "'":
					avatarBase64 = avatarBase64[1:]
					avatarBase64 = avatarBase64[:len(avatarBase64)-1]
				frReqDict['avatar'] = avatarBase64

		emit('status friend request',json.dumps(frReqDict),room=room)
	else: #not needed
		room = data['chat_token']
		emit('bad friend request','Invalid email',room=room)


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


@socketio.on('remove friend',namespace='/chat')
def remove_friend(data):
	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	friendshipIdString = data['friendship_id']

	if friendshipIdString != None:
		friendshipID = int(friendshipIdString)

		query = "SELECT id FROM users WHERE chat_token = '%s'" % (data['chat_token'])
		cursor.execute(query)
		result = cursor.fetchone()
		if result != None:
			uid1 = result[0]
			query = "SELECT user_1,user_2 FROM friendships WHERE (user_1 = '%d' OR user_2='%d') AND id='%d' " % (uid1,uid1, friendshipID)
			cursor.execute(query)
			result = cursor.fetchone()

			if result != None:

				"""f = open("socketio-error.log","a")
				f.write(data['chat_token'] + " " + data['friendship_id'] + "\n")
				f.close()"""


				uid2 = result[0] if result[0] != uid1 else result[1]

				query = "DELETE FROM messages WHERE ((user_1 = '%d' AND user_2 = '%d' ) OR ( user_1 = '%d' AND user_2 = '%d')) " % (uid1, uid2, uid2, uid1)
				cursor.execute(query)
				#db.commit()

				query = "DELETE FROM friendships WHERE id= '%d'" % (friendshipID)
				cursor.execute(query)
				db.commit()

				query = "SELECT chat_token FROM users WHERE id = '%d'" % (uid2)
				cursor.execute(query)
				resultChatToken = cursor.fetchone()
				room = resultChatToken[0]

				removed = {}
				removed["old_friendship_id"] = friendshipID
				removed["message"] = 'Removed from friends'
				emit('friend removed',json.dumps(removed),room=room)
				emit('friend removed',json.dumps(removed),room=data['chat_token'])
				f = open('socketio-error.log','a')
				f.write('friend removed ' + str(friendshipID) + '\n')
				f.close()
			else:
				f = open('socketio-error.log','a')
				f.write('wrong fr id\n')
				f.close()
				emit('bad remove friend','Wrong friendship id',room=data['chat_token'])
		else:
			emit('bad remove friend','Invalid chat token',room=data['chat_token'])
	else:
		emit('bad remove friend','Friendship id not provided',room=data['chat_token'])

@socketio.on('random chat',namespace='/chat')
def random_chat(data):

	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()

	dict = json.loads(str(data))

	query = "SELECT id FROM users where chat_token = '%s'" % (dict['chat_token'])
	cursor.execute(query)
	result = cursor.fetchone()
	uid = result[0]

	query = "SELECT id FROM users WHERE id NOT IN (SELECT user_1 FROM friendships WHERE user_2 = '%d' UNION SELECT user_2 FROM friendships WHERE user_1 = '%d')" % (uid,uid)

	cursor.execute(query)
	userIdsRow = cursor.fetchall()

	userIds = []

#	f = open('socketio-error.log','a')

	for row in userIdsRow:
		userIds.append(row[0])
#		f.write(str(row[0]) + " " )
#	f.write('\n')
#	f.close()

	if uid in userIds:
		userIds.remove(uid)

	randomId = random.choice(userIds)

	randomToken = str(token_encoder.encode_random_token(randomId))
	randomToken = randomToken[2:]
	randomToken = randomToken[:len(randomToken)-1]

	rnd = {}
	rnd["random_token"] = randomToken

	rndSenderToken = str(token_encoder.encode_random_token(uid))
	rndSenderToken = rndSenderToken[2:]
	rndSenderToken = rndSenderToken[:len(rndSenderToken)-1]

	rndSender = {}
	rndSender["random_token"] = rndSenderToken

	query = "SELECT chat_token FROM users where id = '%d'" % (randomId)
	cursor.execute(query)
	result = cursor.fetchone()
	roomR = result[0]

	f = open('socketio-error.log','a')
	f.write('random user id: ' + str(randomId) + '\n')
	f.close()

	emit('random chat token',json.dumps(rnd),room=dict['chat_token'])
	emit('random chat token',json.dumps(rndSender),room=roomR)


@socketio.on_error_default
def default_error_handler(e):
	wr = open('socketio-error.log','a')
	wr.write(str(e) + " pare rau\n")
	wr.close()
