#!/usr/bin/python3

from flask import Blueprint,Response,request
from datetime import datetime
import json
import MySQLdb

#how to retrieve parameters depending on request type:
#email = request.form.get("email") -- if request is POST
#email = request.args.get("email") -- if request is GET

appSignup = Blueprint('api_signup',__name__)

@appSignup.route("/api/signup",methods=['POST']) #methods=['POST']
def signup():
	db = MySQLdb.connect(host="localhost",user="root",passwd="QAZxsw1234",db="linksdb")
	
	email = request.form.get("email")
	password = request.form.get("password")
	name = request.form.get("name")
	birthday_date = request.form.get("birth_day") + "-" + request.form_get("birth_month") + "-" + request.form.get("birth_year")
	birth_date = datetime.strptime(birth_date,'%d-%m-%Y')
	birthday_date = birth_date.strftime('%Y-%m-%d')
	
	
	response = {}
	
	
	cur = db.cursor()
	
	queryCheckUser = "SELECT * FROM users WHERE email='%s'" % (email)
	
	cur.execute(queryCheckUser)
	data = cur.fetchone()
	
	if(data != None)
		query = "INSERT INTO users (email,password,name,birthday_date) VALUES('%s','%s','%s',str_to_date('%s','%%Y-%%m-%%d'))" % (email, password, name, birthday_date)
	
		cur.execute(query)
		db.commit()
		
		response["status"] = 'ok'
		response["email"] = email
		response["password"] = password
		response["name"] = name
		response["birthday_date"] = birthday_date
		
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	db.close()
	
	response["status_code"] = 401
	response["error"] = "Email already taken"
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	
