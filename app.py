from flask import Flask, render_template, request
import json
app = Flask(__name__)

# Temporary, remove import ASAP
from server.session import _ph

# For debugging purposes, remove this during deployment
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Load secrets from disk
with open("secrets/secrets.json") as f:
    secrets = json.loads(f.read())

# Set up database connection
app.config["SQLALCHEMY_DATABASE_URI"] = secrets["dbconnection"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.get("/signup")
def signup_get():
    return render_template("signup.html")

@app.post("/signup")
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    hash = _ph.hash(password)

    return f"{username}\n{hash}"

if __name__ == "__main__":
    app.run()