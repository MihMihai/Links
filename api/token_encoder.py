#!/usr/bin/python3

import jwt

def encode_auth_token(user_id):
	#this may throw an exception if file doesn't exist
	key = read_key_from_file()

	try

		payload = {
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,seconds=300),
			'iat': datetime.datetime.utcnow(),
			'sub': user_id
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e

def encode_chat_token(email):
	#this may throw an exception if file doesn't exist
	key = read_key_from_file()
	
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

def encode_random_token(id):
	#this may throw an exception if file doesn't exist
	key = read_key_from_file()

	try:
		payload = {
			'sub': id,
			'rnd': 1
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e
		
def encode_reset_token(email):
	#this may throw an exception if file doesn't exist
	key = read_key_from_file()
	
	try:
		payload = {
			'em': email
			'reset': 1
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e
		
def encode_delete_token(email):
	#this may throw an exception if file doesn't exist
	key = read_key_from_file()

	try:
		payload = {
			'em': email,
			'delete': 1
		}
		return jwt.encode(payload,
			key,
			algorithm = 'HS256'
		)
	except Exception as e:
		return e

def read_key_from_file():
	f = open('../../server.conf','r')
	key = f.readline()
	f.close()
	return key