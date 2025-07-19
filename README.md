# Blog API - Production Ready

A comprehensive, production-ready Flask-based blog API with enterprise-grade features including monitoring, security, testing, infrastructure as code, and a beautiful modern UI dashboard.

![Blog API Dashboard](pics/home_page.png)

---

## 🚀 Features

### Core Application
- **RESTful API** with CRUD operations for posts and users
- **SQLite Database** with proper schema and migrations
- **Health Checks** for load balancer integration
- **Rate Limiting** to prevent abuse
- **Security Headers** and CORS support

### 🎨 Modern UI Dashboard
- **Web Interface** with Tailwind CSS
- **Real-time Status Monitoring** with live health indicators
- **Interactive API Testing** with one-click endpoint testing
- **Live Response Display** showing JSON responses in real-time
- **Auto-refresh Status** updates every 30 seconds
- **Responsive Design** that works on all devices
- **Professional Dashboard** with gradient backgrounds and animations
- **Quick Action Buttons** for testing all endpoints
- **Visual API Documentation** with endpoint reference
- **Direct Monitoring Links** to Prometheus and Grafana

### Monitoring & Observability
- **Prometheus Metrics** with custom business metrics
- **Grafana Dashboards** for visualization
- **Alerting Rules** for proactive monitoring
- **Structured Logging** for debugging and audit trails
- **Health Check Endpoints** for load balancers

### Security
- **Input Validation** and sanitization
- **Rate Limiting** to prevent DDoS attacks
- **Security Headers** (HSTS, CSP, XSS Protection)
- **CORS Configuration** for frontend integration
- **Password Hashing** (SHA-256, upgrade to bcrypt in production)

### Testing
- **Unit Tests** with pytest
- **Integration Tests** for API endpoints
- **Test Coverage** reporting
- **Security Testing** with Bandit
- **Dependency Scanning** with Safety

### Infrastructure
- **Docker Containerization** with multi-stage builds
- **Kubernetes Manifests** for orchestration
- **Terraform IaC** for AWS infrastructure
- **GitHub Actions CI/CD** with automated testing and deployment
- **Environment Configuration** management

### Performance
- **Caching Layer** with LRU cache
- **Database Connection Pooling**
- **Response Time Monitoring**
- **Resource Usage Tracking**

---

## 🛠 Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Database (upgrade to PostgreSQL in production)
- **Python 3.9+** - Runtime environment

### Frontend & UI
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icon library
- **JavaScript (ES6+)** - Interactive functionality
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations

### Containerization & Orchestration
- **Docker** - Containerization
- **Docker Compose** - Multi-container setup
- **Kubernetes** - Container orchestration

### Infrastructure & DevOps
- **Terraform** - Infrastructure as Code
- **AWS** - Cloud infrastructure (EKS, RDS, ALB)
- **GitHub Actions** - CI/CD pipeline

### Monitoring & Observability
- **Prometheus** - Metrics collection and storage
- **Grafana** - Metrics visualization and dashboards
- **Alertmanager** - Alert management
- **Custom Metrics** - Business-specific monitoring

### Testing & Quality
- **pytest** - Unit and integration testing
- **Bandit** - Security testing
- **Safety** - Dependency vulnerability scanning
- **Coverage** - Test coverage reporting

### Security
- **Rate Limiting** - DDoS protection
- **Input Validation** - Data sanitization
- **Security Headers** - HSTS, CSP, XSS Protection
- **CORS** - Cross-origin resource sharing

---

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+
- kubectl (for Kubernetes deployment)
- Terraform (for infrastructure deployment)

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Destro3998/blog-api.git
cd blog-api

# Start with Docker Compose
docker compose up -d

# Access the application
Dashboard: http://localhost:5050
API: http://localhost:5050/api
Metrics: http://localhost:8000/metrics
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (admin/admin)
```

### Web Dashboard Features

Visit **http://localhost:5050** to access the beautiful dashboard with:

- **📊 Status Cards**: Real-time API and database health
- **🔧 Quick Actions**: Test all endpoints with one click
- **📚 API Documentation**: Visual endpoint reference
- **📈 Monitoring Links**: Direct access to Prometheus/Grafana
- **🔄 Live Results**: See API responses in real-time
- **⚡ Auto-refresh**: Status updates every 30 seconds

### API Endpoints

```bash
# Health check
curl http://localhost:5050/health

# Get all posts
curl http://localhost:5050/api/posts

# Create a post
curl -X POST http://localhost:5050/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Content","author":"John Doe"}'

# Get all users
curl http://localhost:5050/api/users

# Create a user
curl -X POST http://localhost:5050/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}'
```

---

## 🏗 Infrastructure Deployment

### Using Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

## 🔒 Security Features

- **Rate Limiting**: 100 requests per minute per IP
- **Input Validation**: All inputs are validated and sanitized
- **Security Headers**: HSTS, CSP, XSS Protection
- **CORS**: Configured for frontend integration
- **Password Hashing**: Secure password storage

---

## 📈 Performance

- **Caching**: LRU cache for frequently accessed data
- **Database Optimization**: Connection pooling and query optimization
- **Response Time Monitoring**: Track and alert on slow responses
- **Resource Monitoring**: CPU, memory, and disk usage tracking

---

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Testing**: Unit tests, integration tests, security scans
2. **Building**: Docker image building with caching
3. **Security**: Dependency vulnerability scanning
4. **Deployment**: Automated deployment to staging/production
5. **Monitoring**: Post-deployment health checks
