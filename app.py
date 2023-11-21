from flask import Flask, render_template, request
import json
app = Flask(__name__)

# For debugging purposes, remove this during deployment
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Load secrets from disk
with open("secrets/secrets.json") as f:
    secrets = json.loads(f.read())

# Set up database connection
app.config["SQLALCHEMY_DATABASE_URI"] = secrets["dbconnection"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import server.session as session

@app.get("/signup")
def signup_get():
    return render_template("signup.html")

@app.post("/signup")
def signup_post():
    try:
        new_user = session.signup_user(request)
    except ValueError:
        return "Invalid info"

    if new_user:
        return "Created user"
    else:
        return "Users already existed"

@app.get("/login")
def login_get():
    return render_template("login.html")

@app.post("/login")
def login_post():
    try:
        user = session.login_user(request)
    except ValueError:
        return "Invalid info"

    if user:
        return "Signed in"
    else:
        return "Sign in failed"

if __name__ == "__main__":
    app.run()