from flask import Flask, jsonify, Response
import socket
import time
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('app_request_count', 'Total app HTTP requests count', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])
ACTIVE_REQUESTS = Gauge('app_active_requests', 'Number of active requests')

@app.before_request
def before_request():
    ACTIVE_REQUESTS.inc()

@app.after_request
def after_request(response):
    ACTIVE_REQUESTS.dec()
    return response

@app.route('/')
def hello():
    start_time = time.time()
    
    hostname = socket.gethostname()
    response = jsonify({
        "message": "Hello from containerized app!",
        "hostname": hostname
    })
    
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    
    return response

@app.route('/health')
def health():
    start_time = time.time()
    
    response = jsonify({
        "status": "healthy"
    })
    
    REQUEST_COUNT.labels('GET', '/health', 200).inc()
    REQUEST_LATENCY.labels('GET', '/health').observe(time.time() - start_time)
    
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)