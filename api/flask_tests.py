import os
import unittest
import json
from flask import Flask,send_from_directory
from flask_login import LoginManager, login_required, current_user
from flask_testing import TestCase
from signup import signup,appSignup
from login import appLogin
from forgotpassword import appForgotPassword
from server import chat,load_user,forgot_password
from User import *

login_manager = LoginManager()

#DOesn't work as intended!!
class MyTests(TestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.template_folder = '/var/www/html'

		app.secret_key  = "q12safj!@#!skdafka"

		login_manager.init_app(app)
		#login_manager.session_protection = 'strong'
		login_manager.login_view = '/'
		login_manager.anonymous_user = Anonymous


		app.register_blueprint(appSignup)
		app.register_blueprint(appLogin)
		app.register_blueprint(appForgotPassword)
		app.add_url_rule('/api/signup','api_signup',signup)
		app.add_url_rule('/chat','chat',chat)
		app.add_url_rule('/forgotpassword','forgotpassword',forgot_password)
		return app

	@login_manager.user_loader
	def load_user(user_id):
		return User.get(user_id)

	def signup(self,email,name,password,birth_day,birth_month,birth_year):
		return self.client.post('/api/signup',data=dict(
			email=email,
			name=name,
			password=password,
			birth_day=birth_day,
			birth_month=birth_month,
			birth_year=birth_year)
		)

	def login(self,email,password):
		return self.client.post('/api/login',data=dict(
			email=email,
			password=password), follow_redirects=True)

	def test_signup(self):
		response = self.signup('test@qwerty.com','Test','12345','26','May','1999')
		self.assertEqual(response.json,dict(status="ok"))

	def test_account_unnactive(self):
		response = self.login('test@qwerty.com','12345')
#		print(response.get_data(as_text=True))
		with open('/var/www/html/account_NotVerified.html') as f:
			acc_unverified = f.read()
		acc_unverified = acc_unverified[:len(acc_unverified)-1]
		self.assertEqual(response.get_data(as_text=True),acc_unverified)

#	def test_chat_page_html(self):
#		response = self.login('test@qwerty.com','12345')
#		with open('/var/www/html/chat.html') as f:
#			chat_page = f.read()
#		chat_page = chat_page[:len(chat_page)-1]
#		self.assertEqual(response.get_data(as_text=True),chat_page)

	def test_forgot_password_html(self):
		response = self.client.get('/forgotpassword')
		data = response.get_data(as_text=True)
		with open('/var/www/html/forgot_password.html') as f:
			forgot_password_page = f.read()
		forgot_password_page = forgot_password_page[:len(forgot_password_page)-1]
		self.assertEqual(data,forgot_password_page)

	def test_forgot_password_api(self):
		response = self.client.post('/api/forgot_password',data=dict(
			email='bmihai04@gmail.com'))
		data = response.get_data(as_text=True)
		my_data = {}
		my_data["status"] = 'ok'
		json_expected = json.dumps(my_data)
		self.assertEqual(data,json_expected)

#		self.assertEqual(response.get_data(as_text=True),send_from_directory('/var/www/html','account_NotVerified.html'))
#		data = json.loads(response.get_data(as_text=True))
#		print(response.get_data(as_text=True))
#		auth_token = data['access_token']
#		profile_response = self.profile()
#		data_profile = json.loads(profile_response.get_data(as_text=True))
#		email = data_profile['email']
#		self.assertEqual(email,'test@qwerty.com')


if __name__ == '__main__':
    unittest.main()
