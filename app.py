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
app.secret_key = secrets["sessionkey"]

import server.session as session
import server.controllers.user as user_controller

""" @app.route("/signup", methods=["GET", "POST"])
def signup_get():
    form = user_controller.SignupForm()
    if form.validate_on_submit():
        try:
            new_user = session.signup_user(request)
        except ValueError:
            return "Invalid info"

        if new_user:
            return "Created user"
        else:
            return "Users already existed"
    return render_template("dummy_signup.html", form=form) """

""" @app.route("/login", methods=["GET", "POST"])
def login_get():
    form = user_controller.LoginForm()
    if form.validate_on_submit():
        try:
            user = session.login_user(request)
        except ValueError:
            return "Invalid info"

        if user:
            return "Signed in"
        else:
            return "Sign in failed"
    return render_template("dummy_login.html", form=form) """

# Temporary debugging, do not keep
@app.get("/<path>")
def wildcard(path):
    return render_template(path)

@app.get("/NinerNav/<path>")
def wildcard_other(path):
    return render_template("NinerNav/" + path)

@app.get("/favicon.ico")
def favicon():
    return "", 404

if __name__ == "__main__":
    app.run()
