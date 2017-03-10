#!/usr/bin/python3
from flask import Blueprint

appLogin = Blueprint('api',__name__)

@appLogin.route("/api/login")
def login():
	return "heei Mihaai"
