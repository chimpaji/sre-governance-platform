from flask import Flask, jsonify, request
import time
import os

app = Flask(__name__)

# Mock data
MOCK_USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "status": "active"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "status": "active"},
    {"id": 3, "name": "Carol Williams", "email": "carol@example.com", "status": "inactive"},
]

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        "status": "healthy",
        "service": "sre-governance-api",
        "version": "1.0.0"
    }), 200


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get users endpoint with chaos engineering support"""
    
    # Chaos Engineering: Simulate latency
    if request.args.get('chaos') == 'latency':
        app.logger.warning("🔥 CHAOS MODE: Injecting 3s latency")
        time.sleep(3)
    
    # Chaos Engineering: Simulate errors
    if request.args.get('chaos') == 'error':
        app.logger.error("🔥 CHAOS MODE: Simulating 500 error")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Chaos engineering - simulated failure"
        }), 500
    
    # Normal response
    return jsonify({
        "users": MOCK_USERS,
        "count": len(MOCK_USERS),
        "timestamp": time.time()
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API documentation"""
    return jsonify({
        "service": "SRE Governance Platform API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "users": "/api/users",
            "chaos_latency": "/api/users?chaos=latency",
            "chaos_error": "/api/users?chaos=error"
        },
        "documentation": "https://github.com/yourusername/sre-governance-platform"
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
