#!/usr/bin/python3

from flask import Blueprint,Response
from flask import request
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
	birthday_date = request.form.get("birthday_date")
	
	response = {}
	response["status"] = 'ok'
	response["email"] = email
	response["password"] = password
	response["name"] = name
	response["birthday_date"] = birthday_date
	
	query = "INSERT INTO users (email,password,name,birthday_date) VALUES('%s','%s','%s',str_to_date('%s','%%Y-%%m-%%d'))" % (email, password, name, birthday_date)

	cur = db.cursor()
	cur.execute(query)
	db.commit()
	
	
	db.close()
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
