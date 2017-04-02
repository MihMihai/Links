#!usr/bin/python3

from flask import Blueprint, Response, request, render_template
import json
import jwt
import MySQLdb

appActivate = Blueprint('api_activate',__name__)

@appActivate.route("/activate", methods = ['GET']) 
def activate():

	#get token from url
	validationToken = request.args.get("token")
	if validationToken == '':
		response["error"] = "Invalid activation token"
		response["description"] = "Missing activation token"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys = True), mimetype = "application/json"), 401
	
	db = MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")
	
	query = "SELECT id FROM users WHERE validation_token = '%s' " % (validationToken)
	cursor = db.cursor()
	cursor.execute(query)
	uid = cursor.fetchone()

	if uid == None: 
		return render_template("activation_failed.html")
	uid = uid[0]
	
	query = "UPDATE users SET active = 1, validation_token = '' WHERE id = '%d' " % (uid)
	cursor.execute(query)
	
	db.commit()
	
	return render_template("activation_successful.html")
	
