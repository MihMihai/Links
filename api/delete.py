#!usr/bin/python3

from flask import Blueprint, Response, request, render_template
import json
import jwt
import MySQLdb

appDelete = Blueprint('api_delete',__name__)

@appDelete.route("/delete", methods = ['GET']) 
def delete():

	#get reset token from url
	deleteToken = request.args.get("token")
	if deleteToken == '':
		response["error"] = "Invalid delete token"
		response["description"] = "Missing delete token"
		response["status_code"] = 401
		return Response(json.dumps(response,sort_keys = True), mimetype = "application/json"), 401
	
	db = MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")
	
	query = "SELECT id FROM users WHERE delete_token = '%s' " % (deleteToken)
	cursor = db.cursor()
	cursor.execute(query)
	uid = cursor.fetchone()[0]
	
	if uid == None: 
		return render_template("delete_failed.html")
	
	query = "DELETE FROM messages WHERE user_1 = '%d' OR user_2 = '%d' " % (uid, uid)
	db.execute(query)
	query = "DELETE FROM friendships WHERE user_1 ='%d' OR user_2 = '%d' " %(uid, uid)
	db.execute(query)
	query = "DELETE FROM users WHERE id = '%d' "  %(uid)
	db.execute(query)
	db.commit()
	
	return render_template("delete_successful.html")
	