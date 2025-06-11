from prometheus_client import start_http_server, Counter
import random

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello from Blog API! - this is v1 update here to test CI/CD"

if __name__ == "__main__":
    start_http_server(8000)  # Prometheus will scrape from here
    app.run(host="0.0.0.0", port=5000)
