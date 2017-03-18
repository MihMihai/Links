#!/usr/bin/python3

from flask import Flask, render_template,Response,send_from_directory
from flask_socketio import SocketIO
import json
from login import appLogin
from signup import appSignup
from friendrequest import appFriendRequest
from acceptfriend import appAcceptFriend
from removefriend import appRemoveFriend
from friendrequests import appFriendRequests
from profile import appProfile
from update import appUpdate
from logout import appLogout

app = Flask(__name__,template_folder='/var/www/html',static_folder='/var/www/html/static')
socketio = SocketIO(app)

app.register_blueprint(appLogin)
app.register_blueprint(appSignup)
app.register_blueprint(appFriendRequest)
app.register_blueprint(appAcceptFriend)
app.register_blueprint(appRemoveFriend)
app.register_blueprint(appFriendRequests)
app.register_blueprint(appProfile)
app.register_blueprint(appUpdate)
app.register_blueprint(appLogout)

@app.route("/api/hello")
def hello():
	user = {}
	user["Nume"] = "Andrei"
	user["Varsta"] = 20
	user["Facultate"] = 'Ongoing'
	user["Master"] = 'False'

	studii = ["Gradinita","Scoala Generala","Liceu","Facultate"];
	user["studii"] = studii

	userJson = json.dumps(user)
	return Response(userJson,mimetype='application/json')

@app.route("/api/name")
def name():
	return "Ahoi marinari!!"

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/chat")
def chat():
	return render_template("chat.html")

@app.route("/js/Roboto-Black.ttf")
def sendFont():
	return send_from_directory('/var/www/html/static/js','Roboto-Black.ttf')

if __name__ == "__main__":
	app.run(debug=True)


