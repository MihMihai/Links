#!/usr/bin/python3
from flask import Blueprint, Response, request
import json
import MySQLdb
import time 

appAcceptFriend = Blueprint('api_acceptfriend',__name__)

@appAcceptFriend.route("/api/accept_friend", methods =['POST'])

def acceptFriend():
	
	db=MySQLdb.connect (host="localhost", user="root", passwd="QAZxsw1234", db="linksdb")
	
	requestID = int(request.form.get("requestID"))
	newDate = time.strftime("%Y-%m-%d")
	response = {}
	cursor = db.cursor()
	query = " UPDATE friendships SET status='%d', date=str_to_date('%s','%%Y-%%m-%%d') WHERE id='%d'" % (1,newDate,requestID)
	cursor.execute(query)
	db.commit()
	response["status"]= "ok"

	db.close()
	return Response(json.dumps(response, sort_keys=True), mimetype="application/json")
