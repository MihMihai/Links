#!/usr/bin/python3

import MySQLdb
from singleton import Singleton

@Singleton
class DbHandler:

	def __init__(self):
		self._connection = None

	def get_connection(self):
		if self._connection == None:
			f = open('../../mysql_db.conf','r')
			password = f.readline()
			password = password[:len(password)-1]
			f.close()
			self._connection = MySQLdb.connect(host="localhost",user="root",passwd=password, db="linksdb")
		return self._connection
