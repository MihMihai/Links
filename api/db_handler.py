#!/usr/bin/python3

import MySQLdb

@Singleton
class DbHandler:
	
	def get_connection():
		f = open('../../mysql_db.conf','r')
		password = f.read()
		f.close()
		return MySQLdb.connect(host="localhost",user="root",passwd=password, db="linksdb")