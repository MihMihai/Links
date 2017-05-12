#!/usr/bin/python3

from flask import request,Response,Blueprint,redirect
from flask_login import login_user
import token_encoder
import MySQLdb
import jwt
from User import *

appUserLogin = Blueprint('userlogin',__name__)

@appUserLogin.route('/login')
def appLoginUser():

	userToken = request.headers.get("Authorization")

	if userToken == None:
		return redirect("/")

	key = token_encoder.read_key_from_file()

	try:
		userAcc = jwt.encode(userToken,key)
	except jwt.ExpiredSignatureError:
		return redirect("/")
	except jwt.InvalidSignatureError:
		return redirect("/")

	rememberMe = request.form.get("remember_me")

	user = User.get(userAcc['sub'])

	if rememberMe == "true":
		login_user(user,remember=True)
	else:
		login_user(user)

	#return redirect("/chat")
	response = {}
	response["redirect"] = "/chat"
	return Response(json.dumps(response),mimetype="application/json")
