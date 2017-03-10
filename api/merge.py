#!/usr/bin/python3

import json

print("Content-type:application/json\r\n\r\n")
print()
user = {}
user["Nume"] = "Andrei"
user["Varsta"] = 20
user["Facultate"] = 'Ongoing'
user["Master"] = 'False'

studii = ["Gradinita","Scoala Generala","Liceu","Facultate"];
user["studii"] = studii

userJson = json.dumps(user)
print(userJson)