#!/usr/bin/python3
from flask import Blueprint,request
import MySQLdb

appLogin = Blueprint('api_login',__name__)

@appLogin.route("/api/login", methods =['POST']) #methods=['POST']
def login():
	
	db= MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")

	email = request.form.get("email")
	password = request.form.get("password")
	
	#query =  "SELECT EMAIL, PASSWORD FROM USERS WHERE EMAIL= %s AND PASSWORD = %s" % (email, password)
	
	cursor = db.cursor()
	
	cursor.execute("SELECT VERSION()")
	
	data = cursor.fetchone()

	# disconnect from server
	db.close()
	
	return "Database version : %s " % data

	
