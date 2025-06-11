# Blog API

A Flask-based blog API with Prometheus + Grafana monitoring, Dockerized and orchestrated via Docker Compose. CI/CD handled through GitHub Actions.

---

## Tech Stack

- **Flask** – Python web app
- **Docker** – Containerization
- **Docker Compose** – Multi-container setup
- **Prometheus** – Metrics scraping
- **Grafana** – Metrics visualization
- **GitHub Actions** – CI/CD pipeline

---

## Setup

### Clone & Build

git clone https://github.com/Destro3998/blog-api.git
cd blog-api
docker build -t destro3998/blog-api:latest .
docker push destro3998/blog-api:latest
docker compose up


API: http://localhost:5050
Metrics: http://localhost:8000/metrics

![Prometheus Metrics] (pics/prometheus_metrics.png)

Prometheus: http://localhost:9090

![Prometheus UI] (pics/prometheus_target_status.png)

Grafana: http://localhost:3000 (admin/admin - username/password)

![Grafana Dashbaord] (pics/grafana_dashboard.png)

### CI/CD Pipeline

On changes commit and push, GitHub Actions will:
- Builds Docker image
- Pushes to Docker Hub: destro3998/blog-api

### Observability

Prometheus scrapes metrics from /metrics
Grafana visualizes request counts and trends
