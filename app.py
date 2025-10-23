from flask import Flask
import redis
import time

app = Flask(__name__)

# Connect to Redis server (using service name from docker-compose)
r = redis.Redis(host='redis-server', port=6379, decode_responses=True)

@app.route('/')
def home():
    # Check if cached data exists
    data = r.get('home')
    
    if data is not None:
        cached_data = eval(data)  # Convert string back to dict
        # Check if cache is less than 10 minutes old (600 seconds)
        if time.time() - cached_data['time'] < 600:
            return cached_data['html']
    
    # Generate new HTML
    html = '''
    <html>
        <head><title>Flask App with Redis Cache</title></head>
        <body>
            <h1>Hello from Docker Compose!</h1>
            <p>This page is cached with Redis</p>
            <p>Page generated at: ''' + time.strftime('%Y-%m-%d %H:%M:%S') + '''</p>
            <a href="/about">About Page</a>
        </body>
    </html>
    '''
    
    # Store in Redis cache
    r.set('home', str({'html': html, 'time': time.time()}))
    return html

@app.route('/about')
def about():
    # Check if cached data exists
    data = r.get('about')
    
    if data is not None:
        cached_data = eval(data)
        # Check if cache is less than 10 minutes old
        if time.time() - cached_data['time'] < 600:
            return cached_data['html']
    
    # Generate new HTML
    html = '''
    <html>
        <head><title>About - Flask with Redis</title></head>
        <body>
            <h1>About Page</h1>
            <p>This Flask app uses Redis for caching</p>
            <p>Cache expires after 10 minutes</p>
            <p>Page generated at: ''' + time.strftime('%Y-%m-%d %H:%M:%S') + '''</p>
            <a href="/">Home Page</a>
        </body>
    </html>
    '''
    
    # Store in Redis cache
    r.set('about', str({'html': html, 'time': time.time()}))
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
