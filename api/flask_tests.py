import os
import unittest
import json
from flask import Flask,send_from_directory
from flask_testing import TestCase
from signup import signup,appSignup
from login import appLogin
from profile import appProfile

#DOesn't work as intended!!
class MyTests(TestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.template_folder = '/var/www/html'
		app.register_blueprint(appSignup)
		app.register_blueprint(appLogin)
		app.register_blueprint(appProfile)
		app.add_url_rule('/api/signup','api_signup',signup)
		return app

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
			password=password)
		)

#	def test_signup(self):
#		response = self.signup('test@qwerty.com','Test','12345','26','May','1999')
#		self.assertEqual(response.json,dict(status="ok"))

	def profile(self,auth_token):
		return self.client.get(headers={'Authorization':auth_token})

	def test_profile(self):
		response = self.login('test@qwerty.com','12345')
#		print(response.get_data(as_text=True))
		with open('/var/www/html/account_NotVerified.html') as f:
			self.assertEqual(response.get_data(as_text=True),f.read())
#		self.assertEqual(response.get_data(as_text=True),send_from_directory('/var/www/html','account_NotVerified.html'))
#		data = json.loads(response.get_data(as_text=True))
#		print(data)
#		auth_token = data['access_token']
#		profile_response = self.profile()
#		data_profile = json.loads(profile_response.get_data(as_text=True))
#		email = data_profile['email']
#		self.assertEqual(email,'test@qwerty.com')


if __name__ == '__main__':
    unittest.main()
