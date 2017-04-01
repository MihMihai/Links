#!/usr/bin/python3
from flask_login import UserMixin, AnonymousUserMixin
import MySQLdb

class User(UserMixin):
	def __init__(self,id,name,email,active=True):
		self.id = id
		self.name = name
		self.email = email
		self.active = active

	@property
	def is_active(self):

#		f = open('remember_testing.log','a')
#		f.write(str(self.id) + " " + self.name + " " + self.email + " " + str(self.active) + "\n")
#		f.close()

		return True
		#return self.active

	@property
	def is_authenticated(self):
		return True

	@staticmethod
	def get(id):
		db = MySQLdb.connect(host="localhost",user="root", passwd="QAZxsw1234", db="linksdb")
		query = "SELECT name,email FROM users where id = '%s'" % (id)
		cursor = db.cursor()
		cursor.execute(query)
		data = cursor.fetchone()

#		f = open('remember_testing.log','a')
#		f.write(id + ' ' + data[0] + ' ' + data[1] + '\n')
#		f.close()

		if data != None:
			user = User(id,data[0],data[1])
			return user
		else:
			return None

class Anonymous(AnonymousUserMixin):
	name = u"Anonymous"
	email = u"anonymous@gues.com"
