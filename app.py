
from flask import Flask

app = Flask(__name__)
visits = 0

@app.route("/")
def home():
    global visits
    visits += 1
    return f"""
    <h1>Welcome to Class 28!</h1>
    <h2>Visitor Counter Application</h2>
    <p>Website Visits: {visits}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
