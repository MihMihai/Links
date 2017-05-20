#!/usr/bin/python3
from flask import Blueprint,Response,request,redirect,url_for,render_template
from flask_login import logout_user,current_user, login_required
from db_handler import DbHandler
from error_response import ErrorResponse
import token_encoder
import json
import jwt

appLogout = Blueprint('api_logout',__name__)

@appLogout.route("/api/logout", methods =['GET']) #methods=['POST']
@login_required
def logout():
#	userToken = request.headers.get("Authorization")
#	response={}

#	if userToken == None:
#		return ErrorResponse.authorization_required()

#	key = token_encoder.read_key_from_file()

#	try:
#		userAcc = jwt.decode(userToken,key)
#	except jwt.ExpiredSignatureError:
#		return ErrorResponse.token_expired()
#	except jwt.InvalidTokenError:
#		return ErrorResponse.invalid_token()

	query = " UPDATE users SET online = 0 WHERE ID = '%s'" % (current_user.id)

	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()

	logout_user()
	return redirect("/")

#	response["status"] = 'ok'
#	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
