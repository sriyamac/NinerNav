from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

# For debugging purposes, remove this during deployment
app.config["TEMPLATES_AUTO_RELOAD"] = True

# DEBUGGING ONLY, REMOVE BEFORE FINAL SUBMISSION
# This disables HTTP only cookies, making them accessible via JavaScript
# In turn, this makes session hijacking easier
app.config['SESSION_COOKIE_HTTPONLY'] = False

# Load secrets from disk
with open("secrets/secrets.json") as f:
    secrets = json.loads(f.read())

# Set up database connection
app.config["SQLALCHEMY_DATABASE_URI"] = secrets["dbconnection"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets["sessionkey"]

from server.models.models import init_db
import server.controllers.session as session_controller
import server.controllers.user as user_controller
import server.controllers.game as game_controller

@app.route("/", methods=["GET", "POST"])
def index():
    form = user_controller.LoginForm()
    # If a form was submitted (i.e., this is a POST) and was valid, this check passes
    if form.validate_on_submit():
        try:
            user = session_controller.login_user(request)
        except ValueError:
            return "Invalid info"

        if user:
            #return "Signed in"
            pass
        else:
            return "Sign in failed"

    # Determine if the user is signed in
    if session_controller.is_user_authenticated():
        return render_template("index.html", is_authed=True)
    else:
        # TODO: display errors based on exactly how the sign in attempt failed if need be
        return render_template("index.html", is_authed=False, form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Prevent access to page if already signed in
    if session_controller.is_user_authenticated():
        return redirect("/")

    form = user_controller.SignupForm()
    # If a form was submitted (i.e., this is a POST) and was valid, this check passes
    if form.validate_on_submit():
        # Attempt to sign the user up
        try:
            new_user = session_controller.signup_user(request)
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

@app.route("/gamepage", methods=["GET", "POST"])
def gamepage():
    # Mark the game as started (STARTED)
    game_controller.start_game()

    form = game_controller.GPSForm()
    if form.validate_on_submit():
        # Move to the next state (SUBMITTED)
        game_controller.next_state()

        lat, long = form.latitude.data, form.longitude.data

        return "ok"

    return render_template("gamepage.html", form=form)

@app.get("/NinerNav/game")
def ninernav_game():
    return render_template("NinerNav/game.html")

@app.get("/NinerNav/map")
def ninernav_map():
    return render_template("NinerNav/map.html")

@app.get("/leaderboard")
def leaderboard():
    # Get the leaderboard
    scores = game_controller.get_leaderboard()

    return render_template("leaderboard.html", scores=scores)

@app.get("/resultpage")
def resultpage():
    # Require that the state be SUBMITTED
    if not game_controller.is_in_state(game_controller.GameState.SUBMITTED):
        return redirect(url_for("index"))

    # TODO: Process submitted data, including database operations

    # Move from SUBMITTED to PROCESSED
    game_controller.next_state()

    return render_template("resultpage.html")

@app.get("/endgame")
def endgame():
    # Require that the state be PROCESSED
    if not game_controller.is_in_state(game_controller.GameState.PROCESSED):
        return redirect(url_for("index"))

    # Move from PROCESSED to FINISHED
    game_controller.next_state()

    return render_template("end-game.html")

@app.get("/favicon.ico")
def favicon():
    return "", 404

with app.app_context():
    init_db(app)
    game_controller.init_game_info()

if __name__ == "__main__":
    app.run()