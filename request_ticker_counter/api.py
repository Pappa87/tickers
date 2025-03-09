from gevent.pywsgi import WSGIServer
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, HTTP!"

if __name__ == "__main__":
    # Host and port for the HTTP server
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
