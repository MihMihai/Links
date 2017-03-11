#!/usr/bin/python3
from flask import Blueprint,request
import MySQLdb

appLogin = Blueprint('api_login',__name__)

@appLogin.route("/api/login", methods =['POST']) #methods=['POST']
def login():
	
	db= MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")
	
	status = "error"
	email = request.form.get("email")
	password = request.form.get("password")
	
	query =  "SELECT email, password FROM users WHERE email='%s' AND password ='%s'" % (email, password)
	
	cursor = db.cursor()
	cursor.execute(query)
	
	data = cursor.fetchone()
	
	if data != None:
		status = "ok"
	
	# disconnect from server
	db.close()
	
	return status

	
