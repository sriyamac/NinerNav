from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/", methods=["GET", "POST"])
def index():
    """ form = user_controller.LoginForm()
    return render_template("index.html", form=form) """
    form = user_controller.LoginForm()
    # If a form was submitted (i.e., this is a POST) and was valid, this check passes
    if form.validate_on_submit():
        try:
            user = session.login_user(request)
        except ValueError:
            return "Invalid info"

        if user:
            return "Signed in"
        else:
            return "Sign in failed"
    # TODO: display errors based on exactly how the sign in attempt failed if need be
    return render_template("index.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = user_controller.SignupForm()
    # If a form was submitted (i.e., this is a POST) and was valid, this check passes
    if form.validate_on_submit():
        # Attempt to sign the user up
        try:
            new_user = session.signup_user(request)
        except ValueError:
            return "Invalid info"

        if new_user:
            return redirect(url_for("index"))
        else:
            return "Users already existed"
    # TODO: display errors based on exactly how the sign up attempt failed if need be
    return render_template("sign-up.html", form=form)

@app.get("/gameprep")
def gameprep():
    return render_template("gameprep.html")

@app.get("/gamepage")
def gamepage():
    return render_template("gamepage.html")

@app.get("/NinerNav/game")
def ninernav_game():
    return render_template("NinerNav/game.html")

@app.get("/NinerNav/map")
def ninernav_map():
    return render_template("NinerNav/map.html")

@app.get("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.get("/resultpage")
def resultpate():
    return render_template("resultpage.html")

@app.get("/endgame")
def endgame():
    return render_template("end-game.html")

@app.get("/favicon.ico")
def favicon():
    return "", 404

if __name__ == "__main__":
    app.run()
