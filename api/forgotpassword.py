#!usr/bin/python3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template #templating email
from flask import Blueprint, Response, request
from db_handler import DbHandler

import json
import jwt
import smtplib

appForgotPassword = Blueprint('api_forgotpassword',__name__)

@appForgotPassword.route("/api/forgot_password",methods = ['POST'])
def forgotPassword():

	#store credentials for Links Email
	LinksEmail = "linkspeople.chat@gmail.com"
	LinksPassword = "Qw3R$mimaB*"

	#the response to return
	response = {}

	#connect to db
	db = DbHandler.get_instance().get_connection()

	#get email from request
	userEmail = request.form.get("email")

	#if no email received, error
	if userEmail == None:
		response["error"] = "Invalid email"
		response["description"] = "Please provide an email"
		response["status_code"] = 400
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),400


	#get user name based on email
	query = "SELECT name FROM users WHERE email = '%s'" % (userEmail)
	cursor = db.cursor()
	cursor.execute(query)

	userData = cursor.fetchone()

	#check if given email is registered, so in db
	if userData == None:
		response["error"] = "Invalid email"
		response["description"] = "There is no user registered with this email"
		response['status_code'] = 401
		return Response(json.dumps(response,sort_keys=True),mimetype="application/json"),401

	userName = userData[0]

	#set up message body

	#get template text for email, open file
	with open('templates/forgot_email.txt', 'r', encoding='utf-8') as template_file:
	        template_file_content = template_file.read()
	message_template = Template(template_file_content)


	#we generate the token based on user Mail
	resetToken = str(encode_reset_token(userEmail))

	#why not just auth_token[2:len(auth_token) - 1] ??

	resetToken = resetToken[2:]
	resetToken = resetToken[:len(resetToken) - 1]

	#add the token in db for security reason
	#when a user accesses the link, we will check if the token is there
	#if it isn't, it means that it was used already
	query = "UPDATE users SET reset_pass_token = '%s' WHERE email = '%s'" %(resetToken,userEmail)
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()

	#substitute values in template message for customized email
	message = message_template.substitute(USER_NAME = userName, TOKEN = resetToken)

	#set up smtp object to send email
	mailServer = smtplib.SMTP("smtp.gmail.com",587)
	mailServer.starttls()

	# need to find which are these:
	mailServer.login(LinksEmail,LinksPassword)

	#create a mail
	mail = MIMEMultipart()

	#set up parameters
	mail['From'] = LinksEmail
	mail['To'] = userEmail
	mail['Subject'] = "Reset password - Claim your Links back"

	#add message body
	mail.attach(MIMEText(message,'plain'))

	#send mail
	mailServer.sendmail(LinksEmail,userEmail,mail.as_string())

	#tidy up
	mailServer.quit()

	response['status'] = "ok"

	return Response(json.dumps(response,sort_keys = True), mimetype = "application/json")

def encode_reset_token(email):
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



