from flask import Flask
app = Flask(__name__)
@app.route('/')
def say_hello():
	return '<p>WELCOME! This is another string!</p> <a href="/about">ABOUT PAGE</a> | <a href="/contact">Contact</a>'
@app.route('/about')
def about():
	return '<p>Hello about</p><a href="https://flask.palletsprojects.com/en/stable/>Flask</a><a href="https://www.python.org/">Python</a>'
@app.route('/contact')
def contact():
	return "Contact me at: C20366171@mytudublin.ie"
