#!/usr/bin/python3
from flask_socketio import join_room, leave_room, send
from flask import Blueprint, Response, request
from flask_socketio import SocketIO,emit,send,join_room,leave_room
import json
import MySQLdb
import time
import jwt
from server import app

#appChat = Blueprint('api_chat',__name__)

socketio = SocketIO(app)

@socketio.on('connect',namespace='/chat')
def connect():
	emit('message','Saluuuuut')

@socketio.on('join', namespace='/chat')
def on_join(data):
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	email = data['email']
	query = "Select chat_token FROM users WHERE email = '%s' " % (email)
	cursor=db.cursor()
	cursor.execute(query)
	token = cursor.fetchone()
	room = token[0]
	db.close()
	join_room(room)
	send(email + ' has entered the room.', room=room)


@socketio.on('leave', namespace='/chat')
def on_leave(data):
	db = MySQLdb.connect(host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	email = data['email']
	query = "Select chat_token FROM users WHERE email = '%s' " % (email)
	cursor=db.cursor()
	cursor.execute(query)
	token = cursor.fetchone()
	room = token[0]
	db.close()
	leave_room(room)
	send(email + ' has left the room.', room=room)

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
