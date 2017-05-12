#!/usr/bin/python3
from flask_login import UserMixin, AnonymousUserMixin
from db_handler import DbHandler

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

	@staticmethod
	def get_chat_token_from_id(id):
		db = DbHandler.get_instance().get_connection()
		query = "SELECT chat_token FROM users WHERE id = '%s' " % (id)
		cursor = db.cursor()
		cursor.execute(query)
		data = cursor.fetchone()
		return data[0]

	@staticmethod
	def get_chat_token_from_email(email):
		db = DbHandler.get_instance().get_connection()
		query = "SELECT chat_token FROM users WHERE email = '%s' " % (email)
		cursor = db.cursor()
		cursor.execute(query)
		data = cursor.fetchone()
		return data[0]

	@staticmethod
	def get_id_from_email(email):
		db = DbHandler.get_instance().get_connection()
		query = "SELECT id FROM users WHERE email = '%s' " % (email)
		cursor = db.cursor()
		cursor.execute(query)
		data = cursor.fetchone()
		return data[0]

	@staticmethod
	def get_id_and_chat_token_from_email(email):
		db = DbHandler.get_instance().get_connection()
		query = "SELECT id,chat_token FROM users WHERE email ='%s'" %(email)
		cursor.execute(query)
		data = cursor.fetchone()
		return data

	@staticmethod
	def get_id_email_name_avatar_from(chat_token):
		db = DbHandler.get_instance().get_connection()
		query = "SELECT id,email,name,avatar FROM users WHERE chat_token = '%s'" % (chat_token)
		cursor.execute(query)
		data = cursor.fetchone()
		return data

class Anonymous(AnonymousUserMixin):
	name = u"Anonymous"
