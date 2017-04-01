#!/usr/bin/python3
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin):
	def __init__(self,id,name,email,active=True):
		self.id = id
		self.name = name
		self.email = email
		self.active = active
	
	def is_active(self):
		return self.active
	
class Anonymous(AnonymousUserMixin):
	name = u"Anonymous"