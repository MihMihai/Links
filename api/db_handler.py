#!/usr/bin/python3

import MySQLdb
from singleton import Singleton

@Singleton
class DbHandler:

	def get_connection(self):
		f = open('../../mysql_db.conf','r')
		password = f.readline()
		password = password[:len(password)-1]
		f.close()
		return MySQLdb.connect(host="localhost",user="root",passwd=password, db="linksdb")
