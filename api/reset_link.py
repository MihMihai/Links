#!usr/bin/python3

from flask import Blueprint, Response, request, render_template
import json
import jwt
import MySQLdb

appResetLink = Blueprint('api_resetlink',__name__)

@appResetLink.route("/reset_link")
def resetLink():

	#get reset token from url
	resetToken = request.args.get("token")
	if resetToken == '':
		response["error"] = "Invalid reset token"
		response["description"] = "Missing reset token"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys = True), mimetype = "application/json"), 400

	return render_template("reset_password.html")
	