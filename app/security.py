from functools import wraps
from flask import request, jsonify, g
import time
import re
from collections import defaultdict
import hashlib

# Rate limiting storage (in production, use Redis)
rate_limit_storage = defaultdict(list)

def rate_limit(limit=100, window=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            
            # Clean old entries
            current_time = time.time()
            rate_limit_storage[client_ip] = [
                timestamp for timestamp in rate_limit_storage[client_ip]
                if current_time - timestamp < window
            ]
            
            # Check if limit exceeded
            if len(rate_limit_storage[client_ip]) >= limit:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': window
                }), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_input(data, required_fields, field_types=None):
    """Validate input data"""
    if not isinstance(data, dict):
        return False, "Data must be a JSON object"
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not data[field] or not str(data[field]).strip():
            return False, f"Field {field} cannot be empty"
    
    # Check field types if specified
    if field_types:
        for field, expected_type in field_types.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    return False, f"Field {field} must be of type {expected_type.__name__}"
    
    return True, None

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return text
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', str(text))
    return text.strip()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username format"""
    # Username should be 3-20 characters, alphanumeric and underscores only
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

def log_security_event(event_type, details):
    """Log security events"""
    import logging
    logger = logging.getLogger('security')
    logger.warning(f"Security event: {event_type} - {details}")

def hash_password(password):
    """Hash password using SHA-256 (use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password hash"""
    return hash_password(password) == hashed 