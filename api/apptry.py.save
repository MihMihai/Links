#!/usr/bin/python3

from flask import Flask,Response
import json

app = Flask(__name__)

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

if __name__ == "__main__":
	app.run(debug=True)
