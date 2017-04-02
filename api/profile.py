#!/usr/bin/python3

from flask import Blueprint,Response,request
import json
import MySQLdb
import jwt


appProfile = Blueprint('api_profile',__name__)

@appProfile.route("/api/profile",methods=['GET'])
def friendRequests():
	response = {}

	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234", db="linksdb")

	userToken = request.headers.get("Authorization")

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

	query = " SELECT name, email, birthday_date,chat_token FROM users where ID = '%s'" % (userAcc["sub"])

	cursor = db.cursor()
	cursor.execute(query)
	data = cursor.fetchone()

	response['name']=data[0]
	response['email']=data[1]
	response['birthday_date']=data[2].strftime('%Y-%m-%d')
	response['chat_token'] = data[3]
	response['status']='ok'
	db.close()
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")


