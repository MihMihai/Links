#!/usr/bin/python3
from flask import Blueprint,Response,request,redirect,url_for,render_template
from db_handler import DbHandler
from error_response import ErrorResponse
import json
import jwt

appLogout = Blueprint('api_logout',__name__)

@appLogout.route("/api/logout", methods =['POST']) #methods=['POST']
def logout():
	userToken = request.headers.get("Authorization")
	response={}

	if userToken == None:
		return ErrorResponse.authorization_required()

	f = open('server.conf','r')
	key = f.readline()

	try:
		userAcc = jwt.decode(userToken,key)
	except jwt.ExpiredSignatureError:
		return ErrorResponse.token_expired()
	except jwt.InvalidTokenError:
		return ErrorResponse.invalid_token()

	query = " UPDATE users SET auth_token = null WHERE ID = '%s'" % (userAcc["sub"])

	db = DbHandler.get_instance().get_connection()
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	response["status"] = 'ok'
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
