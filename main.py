import time
import json
import logging
import threading
import os
import requests
from flask import Flask, render_template, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple implementation for testing
class DistributedExecutor:
    def __init__(self, secret):
        self.peer_registry = self.PeerRegistry()
        logger.debug("Initialized dummy DistributedExecutor")

    class PeerRegistry:
        def list_peers(self):
            return [{'ip': '127.0.0.1', 'port': 7520}]

    def submit(self, func, *args):
        return self.FutureResult(func(*args))

    class FutureResult:
        def __init__(self, result):
            self._result = result

        def result(self):
            return self._result

    def shutdown(self):
        pass

executor = DistributedExecutor("test_secret")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Template error: {str(e)}")
        return "Internal Server Error", 500

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
            
        message = data.get('message')
        if not message:
            return jsonify({"error": "Message is required"}), 400

        logger.debug(f"Received message: {message}")
        
        # Simulate broadcast
        peers = executor.peer_registry.list_peers()
        logger.debug(f"Sending to {len(peers)} peers")
        
        return jsonify({
            "status": "success",
            "message": f"Message '{message[:20]}...' sent to {len(peers)} peers"
        })
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

def run_flask():
    app.run(host='0.0.0.0', port=7540, debug=False)

if __name__ == '__main__':
    logger.info("Starting application...")
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        executor.shutdown()
        logger.info("Application stopped")
