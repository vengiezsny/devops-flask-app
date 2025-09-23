#!/bin/bash

sudo apt -y update && sudo apt -y upgrade
sudo apt -y install nano vim python-is-python3
sudo apt -y install python3-venv python3-pip
python -m venv .my_venv
source .my_venv/bin/activate
pip install flask
cat << zz > hello1.py
from flask import Flask
app = Flask(__name__)
@app.route('/')
def say_hello():
	return '<p>Hello, World,I am a Flask app!</p> <a href="/about">ABOUT PAGE</a>'
@app.route('/about')
def about():
	return '<p>Hello about</p>'
zz
flask --app hello run --host=0.0.0.0
