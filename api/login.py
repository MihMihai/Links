#!/usr/bin/python3
from flask import Blueprint,Response,request,redirect,url_for,render_template
from flask_login import login_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db_handler import DbHandler
import token_encoder
import json
import jwt
import datetime
from User import *

appLogin = Blueprint('api_login',__name__)

@appLogin.route("/api/login", methods =['POST']) #methods=['POST']
def login():

	db= DbHandler.get_instance().get_connection()

	response = {}

	#get the info from request
	email = request.form.get("email")
	password = request.form.get("password")
#	rememberMe = request.form.get("remember_me")

	if "remember_me" in request.form:
		rememberMe = True
	else:
		rememberMe = False

	#SQL cmd
	query =  "SELECT id, name, active,password  FROM users WHERE email='%s'" % (email)

	#execute SQL cmd
	cursor = db.cursor()
	cursor.execute(query)

	#retrieve DB answer
	data = cursor.fetchone()

	if data != None:

		pass_from_db = str(data[3])

		if check_password_hash(pass_from_db,password):
			user = User(data[0],data[1],email)
			active = data[2]
			if active == 0:
				return render_template("account_NotVerified.html")
			response["status"] = 'ok'
			if rememberMe == "true":
				login_user(user,remember = True)
			else:
				login_user(user)
		else:
			response["error"] = 'Invalid email or password'
			response["status_code"] = 401
	else:
		response["error"] = 'Invalid email or password'
		response["status_code"] = 401


	#return redirect(urlfor("api_login.chat"))

	if "error" in response:
		return Response(json.dumps(response, sort_keys=True), mimetype="application/json"),401

	auth_token = str(token_encoder.encode_auth_token(data[0]))
	auth_token = auth_token[2:]
	auth_token = auth_token[:len(auth_token)-1]
	response["access_token"] = auth_token

	query = "UPDATE users SET auth_token = '%s' WHERE id = %d" % (auth_token,data[0])

	cursor.execute(query)
	db.commit()

	return redirect("/chat")
	#return redirect(url_for("chat"))
#	return Response(json.dumps(response, sort_keys=True), mimetype="application/json")

#@appLogin.route("/chat")
#def chat():
#	return render_template("index2.html")
