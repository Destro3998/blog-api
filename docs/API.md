# Blog API Documentation

## Overview

The Blog API is a RESTful service built with Flask that provides endpoints for managing blog posts and users. It includes comprehensive monitoring with Prometheus metrics and health checks.

## Base URL

```
http://localhost:5050
```

## Authentication

Currently, the API does not require authentication. In a production environment, you should implement JWT or OAuth2 authentication.

## Endpoints

### 1. Home

**GET** `/`

Returns basic information about the API.

**Response:**
```json
{
  "message": "Blog API v2.0",
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "endpoints": {
    "posts": "/api/posts",
    "users": "/api/users",
    "health": "/health",
    "metrics": "/metrics"
  }
}
```

### 2. Health Check

**GET** `/health`

Returns the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 3. Posts

#### Get All Posts

**GET** `/api/posts`

Returns all blog posts.

**Response:**
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Sample Post",
      "content": "This is the content of the post",
      "author": "John Doe",
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:00:00.000Z"
    }
  ],
  "count": 1
}
```

#### Create Post

**POST** `/api/posts`

Creates a new blog post.

**Request Body:**
```json
{
  "title": "New Post Title",
  "content": "This is the content of the new post",
  "author": "Jane Doe"
}
```

**Response:**
```json
{
  "message": "Post created successfully",
  "id": 2
}
```

#### Get Single Post

**GET** `/api/posts/{id}`

Returns a specific blog post by ID.

**Response:**
```json
{
  "id": 1,
  "title": "Sample Post",
  "content": "This is the content of the post",
  "author": "John Doe",
  "created_at": "2024-01-01T12:00:00.000Z",
  "updated_at": "2024-01-01T12:00:00.000Z"
}
```

### 4. Users

#### Get All Users

**GET** `/api/users`

Returns all users.

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "created_at": "2024-01-01T12:00:00.000Z"
    }
  ],
  "count": 1
}
```

#### Create User

**POST** `/api/users`

Creates a new user.

**Request Body:**
```json
{
  "username": "janedoe",
  "email": "jane@example.com"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "id": 2
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 404 Not Found
```json
{
  "error": "Post not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Metrics

The API exposes Prometheus metrics at `/metrics` endpoint. Available metrics include:

- `http_requests_total`: Total HTTP requests by method and endpoint
- `http_request_duration_seconds`: HTTP request duration
- `active_users`: Number of active users
- `database_connections`: Number of database connections

## Rate Limiting

Currently, the API does not implement rate limiting. In production, consider implementing rate limiting using Flask-Limiter.

## CORS

The API supports CORS (Cross-Origin Resource Sharing) for frontend integration.

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Monitoring

The API includes comprehensive monitoring:

1. **Health Checks**: `/health` endpoint for load balancer health checks
2. **Metrics**: Prometheus metrics for monitoring and alerting
3. **Logging**: Structured logging for debugging and audit trails
4. **Error Handling**: Proper error responses with appropriate HTTP status codes 