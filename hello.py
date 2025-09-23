from flask import Flask
app = Flask(__name__)
@app.route('/')
def say_hello():
	return '<p>Hello, World,I am a Flask app!</p> <a href="/about">ABOUT PAGE</a>'
@app.route('/about')
def about():
	return '<p>Hello about</p>'
