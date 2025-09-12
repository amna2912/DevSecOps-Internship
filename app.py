from flask import Flask, request, jsonify
import logging
import random
import time
import socket
import json
from datetime import datetime

app = Flask(__name__)

# Configure JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'hostname': socket.gethostname(),
            'source': 'flask_app'
        }
        
        # Add request information if available
        try:
            if request:
                log_data['ip'] = request.remote_addr
                log_data['endpoint'] = request.path
                log_data['method'] = request.method
                log_data['user_agent'] = request.headers.get('User-Agent', 'Unknown')
        except RuntimeError:
            log_data['ip'] = socket.gethostbyname(socket.gethostname())
            log_data['endpoint'] = 'internal'
            
        # Add any extra fields
        if hasattr(record, 'username') and record.username:
            log_data['username'] = record.username
        if hasattr(record, 'status_code') and record.status_code:
            log_data['status_code'] = record.status_code
            
        return json.dumps(log_data)

# Set up logger
logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent duplicate logs

# Remove existing handlers
logger.handlers = []

# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)

@app.route('/')
def home():
    logger.info("Home page accessed", extra={'status_code': 200})
    return "Welcome to Windows Flask Logging App!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', 'unknown')
    
    # 30% chance of failure
    if random.random() < 0.3:
        logger.warning("Login failed attempt", extra={
            'username': username,
            'status_code': 401
        })
        return jsonify({"message": "Login failed"}), 401
    
    logger.info("Login successful", extra={
        'username': username,
        'status_code': 200
    })
    return jsonify({"message": "Login successful"})

@app.route('/products')
def products():
    # 10% chance of server error
    if random.random() < 0.1:
        logger.error("Database connection failed", extra={'status_code': 500})
        return jsonify({"message": "Internal server error"}), 500
    
    logger.info("Products accessed", extra={'status_code': 200})
    return jsonify({"products": ["Product A", "Product B", "Product C"]})

@app.route('/generate_logs')
def generate_logs():
    """Generate various types of logs"""
    # Generate different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Generate log with user context
    users = ["alice", "bob", "charlie", "dave"]
    user = random.choice(users)
    logger.info(f"User {user} performed action", extra={'username': user})
    
    return jsonify({"message": "Logs generated successfully"})

@app.route('/status')
def status():
    logger.info("Status check", extra={'status_code': 200})
    return jsonify({
        "status": "running",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Log startup message
    server_ip = socket.gethostbyname(socket.gethostname())
    logger.info("Flask application starting", extra={
        'ip': server_ip,
        'port': 5000
    })
    
    print("=" * 50)
    print("FLASK LOGGING APPLICATION")
    print("=" * 50)
    print(f"Local: http://localhost:5000")
    print(f"Endpoints:")
    print(f"  GET  /              - Home page")
    print(f"  POST /login         - Login endpoint")
    print(f"  GET  /products      - Products list")
    print(f"  GET  /generate_logs - Generate test logs")
    print(f"  GET  /status        - App status")
    print("=" * 50)
    print("Logs will be written to: app.log")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)