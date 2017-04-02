#!/usr/bin/python3
from flask import Blueprint,Response,request,redirect,url_for #,render_template
from flask_login import login_user,current_user
import MySQLdb
import json
import jwt
import datetime
from User import *

appLogin = Blueprint('api_login',__name__)

@appLogin.route("/api/login", methods =['POST']) #methods=['POST']
def login():

	db= MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")

	response = {}

	#get the info from request
	email = request.form.get("email")
	password = request.form.get("password")
	rememberMe = request.form.get("remember_me")

	#SQL cmd
	query =  "SELECT id,name,email, password FROM users WHERE email='%s' AND password ='%s'" % (email, password)

	#execute SQL cmd
	cursor = db.cursor()
	cursor.execute(query)

	#retrieve DB answer
	data = cursor.fetchone()

	if data != None:
#		user = User(data[0],data[1],data[2])
		response["status"] = 'ok'

#		if rememberMe == "true":
#			login_user(user,remember = True)
#		else:
#			login_user(user)
	else:
		response["error"] = 'Invalid email or password'
		response["status_code"] = 401


	#return redirect(urlfor("api_login.chat"))

	if "error" in response:
		return Response(json.dumps(response, sort_keys=True), mimetype="application/json"),401

	auth_token = str(encode_auth_token(data[0]))
	auth_token = auth_token[2:]
	auth_token = auth_token[:len(auth_token)-1]
	response["access_token"] = auth_token

	query = "UPDATE users SET auth_token = '%s' WHERE id = %d" % (auth_token,data[0])

	cursor.execute(query)
	db.commit()
	db.close()

	#return redirect(url_for("chat"))
	return Response(json.dumps(response, sort_keys=True), mimetype="application/json")

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

#@appLogin.route("/chat")
#def chat():
#	return render_template("index2.html")
