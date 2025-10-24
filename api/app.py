from flask import Flask, jsonify, request
import time
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

app = Flask(__name__)

# Security: Force HTTPS and add security headers
Talisman(app, force_https=False, content_security_policy=None)  # force_https=False for demo

# Rate limiting: Prevent DDoS and abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5000 per day", "1000 per hour"],
    storage_uri="memory://",
    strategy="fixed-window"
)

# Mock data
MOCK_USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "status": "active"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "status": "active"},
    {"id": 3, "name": "Carol Williams", "email": "carol@example.com", "status": "inactive"},
]

@app.route('/health')
@limiter.exempt
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        "status": "healthy",
        "service": "sre-governance-api",
        "version": "1.0.0"
    }), 200


@app.route('/api/users')
@limiter.limit("50 per minute")
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
@limiter.limit("200 per hour")
def root():
    """Root endpoint with API documentation"""
    return jsonify({
        "service": "SRE Governance Platform API",
        "version": "1.0.0",
        "rate_limits": {
            "default": "5000 requests/day, 1000 requests/hour per IP",
            "root": "200 requests/hour",
            "api_users": "50 requests/minute"
        },
        "endpoints": {
            "health": "/health",
            "users": "/api/users",
            "chaos_latency": "/api/users?chaos=latency",
            "chaos_error": "/api/users?chaos=error"
        },
        "security": "Rate limiting enabled, DDoS protection active",
        "documentation": "https://github.com/chimpaji/sre-governance-platform"
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
