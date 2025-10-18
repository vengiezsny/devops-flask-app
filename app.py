from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Docker Container!</h1><p>Lab 5 - Docker and Containers</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
