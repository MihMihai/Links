#!/usr/bin/python3

from flask import Blueprint,Response
import MySQLdb

#how to retrieve parameters depending on request type:
#email = request.form.get("email") -- if request is POST
#email = request.args.get("email") -- if request is GET

appSignup = Blueprint('api',__name__)

@appSignup.route("/api/signup") #methods=['POST']
def signup()
	#db = MySQLdb.connect(host="86.120.51.218",user="root",passwd="QAZxsw1234",db="linksdb")
	
	email = request.form.get("email")
	password = request.form.get("password")
	name = request.form.get("name")
	birthday_date = request.form.get("birthday_date")
	
	response = {}
	response["email"] = email
	response["password"] = password
	response["name"] = name
	response["birthday_date"] = birthday_date
	
	#query = "INSERT INTO USERS (EMAIL,PASSWORD,NAME,BIRTHDAY_DATE) VALUES(%s,%s,%s,%s)" % (email, password, name, birthday_date)
	
	#cur = db.cursor()
	#cur.execute(query)
	
	
	#db.close();
	return Response(json.dumps(response),mimetype="application/json")