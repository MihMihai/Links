#!usr/bin/python3
from flask import Blueprint, Response, request
import json
import MySQLdb
import jwt

appResetPassword = Blueprint('api_resetpassword',__name__)

@appResetPassword.route("/api/reset_password", methods = ['POST']
def resetPassword():
	response = {}

	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234", db="linksdb")

	#get the new password from request
	#and the reset token
	password = request.form.get("password")
	resetToken = request.form.get("resetToken")

	#chech if parameters are good
	if password == None OR resetToken == None: 
		response["error"] = "Bad paramters"
		response["description"] = "Missing paramters"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys = True),mimetype = "application/json"), 400


	#check if reset Token is valid
	if checkResetToken(resetToken,db) != 0:
		response["error"] = "Invalid Reset Token"
		response["description"] = "Token was already used. Request a new one."
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401


	#make the query to update password in database
	query = "UPDATE users SET password = %s WHERE reset_pass_token = %s" % (password, resetToken)

	#commit the query
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()


	#clear the reset token in db for security reason : 
	# be sure that another access on the same link will not reset the pw
	query = "UPDATE users SET reset_pass_token = %s WHERE reset_pass_token = %s" %('null',resetToken)
	cursor.execute(query)
	db.commit()
	
	#close the db
	db.close()

	response["status"] = "ok"
	#return response

	return Response(json.dumps(response, sort_keys = True), mimetype = "application/json")


def checkResetToken(token,db):

	#check if the reset token is in the database a.k.a. it was not used
	query = "SELECT reset_pass_token FROM users WHERE reset_pass_token = %s" % (resetToken)
	cursor = db.cursor()
	cursor.execute(query)
	resetToken = cursor.fetchone()

	# 0 means succes, aka the resetToken is in db
	if token == resetToken :
		return 0

	# otherwise, return 1 -error
	# token in db is null(it was used already)
	# token differs from the one in database
	return 1
