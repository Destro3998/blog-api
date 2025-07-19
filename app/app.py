from prometheus_client import start_http_server, Counter, Histogram, Gauge
import random
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP Request Duration')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
DB_CONNECTIONS = Gauge('database_connections', 'Number of database connections')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return render_template('index.html')

@app.route("/api")
def api_info():
    REQUEST_COUNT.labels(method='GET', endpoint='/api').inc()
    return jsonify({
        "message": "Blog API v2.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "posts": "/api/posts",
            "users": "/api/users",
            "health": "/health",
            "metrics": "/metrics"
        }
    })

@app.route("/health")
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
    try:
        # Check database connectivity
        conn = get_db()
        conn.execute("SELECT 1")
        conn.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return jsonify({
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/posts", methods=['GET'])
def get_posts():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/posts').inc()
    with REQUEST_DURATION.time():
        try:
            conn = get_db()
            cursor = conn.execute("SELECT * FROM posts ORDER BY created_at DESC")
            posts = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return jsonify({"posts": posts, "count": len(posts)})
        except Exception as e:
            logger.error(f"Error fetching posts: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.route("/api/posts", methods=['POST'])
def create_post():
    REQUEST_COUNT.labels(method='POST', endpoint='/api/posts').inc()
    with REQUEST_DURATION.time():
        try:
            data = request.get_json()
            if not data or 'title' not in data or 'content' not in data or 'author' not in data:
                return jsonify({"error": "Missing required fields"}), 400
            
            conn = get_db()
            cursor = conn.execute(
                "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
                (data['title'], data['content'], data['author'])
            )
            conn.commit()
            post_id = cursor.lastrowid
            conn.close()
            
            return jsonify({"message": "Post created successfully", "id": post_id}), 201
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.route("/api/posts/<int:post_id>", methods=['GET'])
def get_post(post_id):
    REQUEST_COUNT.labels(method='GET', endpoint='/api/posts/<id>').inc()
    with REQUEST_DURATION.time():
        try:
            conn = get_db()
            cursor = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
            post = cursor.fetchone()
            conn.close()
            
            if post:
                return jsonify(dict(post))
            else:
                return jsonify({"error": "Post not found"}), 404
        except Exception as e:
            logger.error(f"Error fetching post: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.route("/api/users", methods=['GET'])
def get_users():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/users').inc()
    with REQUEST_DURATION.time():
        try:
            conn = get_db()
            cursor = conn.execute("SELECT * FROM users ORDER BY created_at DESC")
            users = [dict(row) for row in cursor.fetchall()]
            conn.close()
            ACTIVE_USERS.set(len(users))
            return jsonify({"users": users, "count": len(users)})
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.route("/api/users", methods=['POST'])
def create_user():
    REQUEST_COUNT.labels(method='POST', endpoint='/api/users').inc()
    with REQUEST_DURATION.time():
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'email' not in data:
                return jsonify({"error": "Missing required fields"}), 400
            
            conn = get_db()
            cursor = conn.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (data['username'], data['email'])
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return jsonify({"message": "User created successfully", "id": user_id}), 201
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    REQUEST_COUNT.labels(method='GET', endpoint='/404').inc()
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    REQUEST_COUNT.labels(method='GET', endpoint='/500').inc()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    init_db()
    start_http_server(8000)  # Prometheus will scrape from here
    app.run(host="0.0.0.0", port=5000, debug=False)
