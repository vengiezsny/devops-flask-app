from flask import Flask
app = Flask(__name__)
@app.route('/')
def say_hello():
	return '<p>WELCOME!</p> <a href="/about">ABOUT PAGE</a> | <a href="/contact">Contact</a>'
@app.route('/about')
def about():
	return '<p>Hello about</p>'
@app.route('/contact')
def contact():
	return "Contact me at: c20366171@mytudublin.ie"
