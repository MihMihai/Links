#!/usr/bin/python3
from flask import Blueprint,Response,request #,redirect,url_for,render_template
import MySQLdb
import json

appLogin = Blueprint('api_login',__name__)

@appLogin.route("/api/login", methods =['POST']) #methods=['POST']
def login():
	
	db= MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")
	
	response ={}

	#get the info from request
	email = request.form.get("email")
	password = request.form.get("password")
	
	#SQL cmd
	query =  "SELECT email, password FROM users WHERE email='%s' AND password ='%s'" % (email, password)
	
	#execute SQL cmd
	cursor = db.cursor()
	cursor.execute(query)
	
	#retrieve DB answer
	data = cursor.fetchone()
	
	if data != None:
		response["status"] = 'ok'
	else:
		response["error"] = 'Invalid email or password'
		response["status_code"] = 401

	# disconnect from server
	db.close()

	#return redirect(urlfor("api_login.chat"))
	return Response(json.dumps(response, sort_keys=True), mimetype="application/json"),401

#@appLogin.route("/chat")
#def chat():
#	return render_template("index2.html")
