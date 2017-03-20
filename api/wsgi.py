#!/usr/bin/python3

from chat import app,socketio
#from flask import Flask
#from flask_socketio import SocketIO

if __name__ == "__main__":
#	app.run(debug=True)
	socketio.run(app)
