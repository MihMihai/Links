#!usr/bin/python3
from flask import Blueprint, Response, request
import json
import MySQLdb
import jwt

appResetPassword = Blueprint('api_resetpassword',__name__)

@appResetPassword.route("/api/reset_password", methods = ['POST'])
def resetPassword():
	response = {}

	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234", db="linksdb")

	#get the new password from request
	#and the reset token
	password = request.form.get("password")
	resetToken = request.headers.get("Authorization")

	#chech if parameters are good
	if password == None or resetToken == None:
		response["error"] = "Bad paramaters"
		response["description"] = "Missing paramaters"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys = True),mimetype = "application/json"), 400

	 #check if the reset token is in the database a.k.a. it was not used
	query = "SELECT reset_pass_token FROM users WHERE reset_pass_token = '%s' " % (resetToken)
	cursor = db.cursor()
	cursor.execute(query)
	dbToken = cursor.fetchone()

	#check if reset Token is valid
	#tken is not valid if not found in db or null
	if dbToken == None or resetToken == '':
		response["error"] = "Invalid Reset Token"
		response["description"] = "Token was already used. Request a new one."
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401


	#make the query to update password in database
	query = "UPDATE users SET password = '%s' WHERE reset_pass_token = '%s' " % (password, dbToken[0])

	#commit the query
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()


	#clear the reset token in db for security reason :
	# be sure that another access on the same link will not reset the pw
	query = "UPDATE users SET reset_pass_token = '%s' WHERE reset_pass_token = '%s' " %("",dbToken[0])
	cursor.execute(query)
	db.commit()

	#close the db
	db.close()

	response["status"] = "ok"
	#return response

	return Response(json.dumps(response, sort_keys = True), mimetype = "application/json")


