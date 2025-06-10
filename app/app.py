from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Blog API! - this is v1 update here to test CI/CD"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
