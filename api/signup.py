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

	response = {}

	email = request.form.get("email")
	password = request.form.get("password")
	name = request.form.get("name")
	birth_day = request.form.get("birth_day")
	birth_month = request.form.get("birth_month")
	birth_year = request.form.get("birth_year")

	if email == None or password == None or  name == None or birth_day == None or birth_month == None or birth_year == None:
		response["error"] = "Bad parameters"
		response["description"] = "Missing parameters"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),400

	birthday_date = birth_day + "-" + birth_month + "-" + birth_year

	birth_date = datetime.strptime(birthday_date,'%d-%B-%Y')
	birthday_date = birth_date.strftime('%Y-%m-%d')

	cur = db.cursor()

	queryCheckUser = "SELECT * FROM users WHERE email='%s'" % (email)

	cur.execute(queryCheckUser)
	data = cur.fetchone()

	if data == None:
		chatToken = str(encode_chat_token(email))
		chatToken = chatToken[2:]
		chatToken = chatToken[:len(chatToken)-1]
		
		query = "INSERT INTO users (email,password,name,birthday_date,chat_token) VALUES('%s','%s','%s',str_to_date('%s','%%Y-%%m-%%d'),'%s')" % (email, password, name, birthday_date,chatToken)
		cur.execute(query)
		db.commit()

		response["status"] = 'ok'

		return Response(json.dumps(response,sort_keys=True),mimetype="application/json")
	db.close()

	response["description"] = "Email already taken"
	response["status_code"] = 401
	response["error"] = "Invalid email"
	return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401
	
	
def encode_chat_token(email):
	#this may throw an exception if file doesn't exist
	f = open('server.conf','r')
	key = f.readline()

	try:
		payload = {
			'em': email
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e
