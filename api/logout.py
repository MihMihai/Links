#!/usr/bin/python3
from flask import Blueprint,Response,request,redirect,url_for,render_template
import MySQLdb
import json
import jwt

appLogout = Blueprint('api_logout',__name__)

@appLogout.route("/api/logout", methods =['POST']) #methods=['POST']
def logout():
	userToken = request.headers.get("Authorization")
	response={}

	if userToken == None:
		response["error"] = "Request does not contain an access token"
		response["description"] = "Authorization required"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")

	f = open('server.conf','r')
	key = f.readline()

	try:
		userAcc = jwt.decode(userToken,key)
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

	query = " UPDATE users SET auth_token = null WHERE ID = '%s'" % (userAcc["sub"])

	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234", db= "linksdb")
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	db.close()
	response["status"] = 'ok'
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
