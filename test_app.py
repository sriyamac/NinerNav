"""Tests to ensure that the critical functions of the application work.

Run `pytest` in this directory to execute the tests.
"""
import pytest
from sqlalchemy import text
from app import app as flask_app
from server.models.models import db
import server.controllers.game as game_controller
import server.controllers.user as user_controller

@pytest.fixture()
def app():
    # Disable CSRF protection
    game_controller.GPSForm.Meta.csrf = False
    user_controller.LoginForm.Meta.csrf = False
    user_controller.SignupForm.Meta.csrf = False
    user_controller.SignoutForm.Meta.csrf = False

    # Ensure the database is in a consistent state
    with flask_app.app_context():
        with open("tests/data.sql") as f:
            db.drop_all()
            db.create_all()
            for line in f.readlines():
                query = text(line)
                db.session.execute(query)
            db.session.commit()

    yield flask_app

@pytest.fixture()
def client(app):
    return app.test_client()

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username, password):
        return self._client.post(
                "/",
                data={"username": username, "password": password}
            )

    def signout(self):
        return self._client.post(
            "/signout",
            follow_redirects=True
        )

    def signup(self, username, email, password):
        return self._client.post(
            "/signup",
            data={"username": username, "email": email, "password": password}
        )

@pytest.fixture
def auth(client):
    return AuthActions(client)

def test_server_running(client):
    """Verify that the Flask server is running."""
    response = client.get("/")
    assert response.status_code == 200

def test_database_running(app):
    """Verify that the database can be reached."""
    with app.app_context():
        query = text("SELECT 1")
        db.session.execute(query)
    assert True

def test_log_in(auth, client):
    """Verify that users can log in."""
    username = "user1"
    password = "a"

    # Ensure that no user is not already signed in
    response = client.get("/")
    assert "Hello, " not in response.data.decode()

    # Attempt invalid authentication
    response = auth.login(None, None)
    assert username not in response.data.decode()

    response = auth.login(username, None)
    assert username not in response.data.decode()

    response = auth.login(None, password)
    assert username not in response.data.decode()

    # Attempt valid authentication
    response = auth.login(username, password)
    assert username in response.data.decode()

    # Attempt logging in while already signed in, should not override existng session
    response = auth.login("user2", "b")
    assert username in response.data.decode()

def test_log_out(auth, client):
    """Verify that users can sign out."""
    username = "user1"
    password = "a"

    # Ensure that no user is not already signed in
    response = client.get("/")
    assert "Hello, " not in response.data.decode()

    # Log in properly
    response = auth.login(username, password)
    assert username in response.data.decode()

    # Sign out
    response = auth.signout()
    assert username not in response.data.decode()

def test_sign_up(auth, client):
    """Verify that users can sign up."""
    valid_username = "user4"
    long_username = "a"*101
    dupe_username = "user1"

    valid_email = "user4@example.com"
    long_email = "a"*100 + "@example.com"
    bad_email = "user4.example@com"
    dupe_email = "user1@example.com"

    valid_password = "Aaaaaaaaaaaa"
    short_password = "Aaaaaaaaaaa"
    no_upper_password = "aaaaaaaaaaaa"
    no_lower_password = "AAAAAAAAAAAA"

    # Test sign ups with missing data
    response = auth.signup(None, valid_email, valid_password)
    assert user_controller.FailureReason.MISSING_USERNAME.value in response.data.decode()

    response = auth.signup(valid_username, None, valid_password)
    assert user_controller.FailureReason.MISSING_EMAIL.value in response.data.decode()

    response = auth.signup(valid_username, valid_email, None)
    assert user_controller.FailureReason.MISSING_PASSWORD.value in response.data.decode()

    # Test sign ups with invalid username data
    response = auth.signup(long_username, valid_email, valid_password)
    assert user_controller.FailureReason.LONG_USERNAME.value in response.data.decode()

    response = auth.signup(dupe_username, valid_email, valid_password)
    assert user_controller.FailureReason.DUPE_USERNAME.value in response.data.decode()

    # Test sign ups with invalid email data
    response = auth.signup(valid_username, long_email, valid_password)
    assert user_controller.FailureReason.LONG_EMAIL.value in response.data.decode()

    response = auth.signup(valid_username, bad_email, valid_password)
    assert user_controller.FailureReason.BAD_EMAIL.value in response.data.decode()

    response = auth.signup(valid_username, dupe_email, valid_password)
    assert user_controller.FailureReason.DUPE_EMAIL.value in response.data.decode()

    # Test sign ups with invalid password data
    response = auth.signup(valid_username, valid_email, short_password)
    assert user_controller.FailureReason.SHORT_PASSWORD.value in response.data.decode()

    response = auth.signup(valid_username, valid_email, no_upper_password)
    assert user_controller.FailureReason.NO_UPPER_PASSWORD.value in response.data.decode()

    response = auth.signup(valid_username, valid_email, no_lower_password)
    assert user_controller.FailureReason.NO_LOWER_PASSWORD.value in response.data.decode()

    # Test valid sign up
    response = auth.signup(valid_username, valid_email, valid_password)
    assert response.status_code == 302

    # Ensure not signed in after sign up
    response = client.get("/")
    assert "Hello, " not in response.data.decode()

def test_view_leaderboard(client):
    """Verify that the leaderboard has correct information."""
    response = client.get("/leaderboard")
    decoded = response.data.decode()

    # Check against hardcoded test data
    assert "1. user3 (Kennedy) - Score: 10" in decoded
    assert "2. user2 (Barnhardt) - Score: 3" in decoded
    assert "3. user1 (Kennedy) - Score: 2" in decoded
    assert "4. user1 (Barnhardt) - Score: 1" in decoded

def test_game(client):
    """Verify that a game can be completed."""
    # Simulate player actions to start the game
    client.get("/gamepage")
    client.get("/NinerNav/game/")
    with client.session_transaction() as session:
        lat = session.get("map_lat")
        lon = session.get("map_lon")

    # Test submission of coordiantes
    response = client.post("/gamepage", data={"latitude": lat, "longitude": lon})
    assert response.data.decode() == "ok"

    # Ensure scoring happened properly
    response = client.get("/resultpage")
    assert "100 points earned" in response.data.decode()

def test_zero_game(client):
    """Verify that a completely wrong guess gets 0 points."""
    # Simulate player actions to start the game
    client.get("/gamepage")
    client.get("/NinerNav/game/")

    # Test submission of coordiantes
    response = client.post("/gamepage", data={"latitude": 0, "longitude": 0})
    assert response.data.decode() == "ok"

    # Ensure scoring happened properly
    response = client.get("/resultpage")
    assert "0 points earned" in response.data.decode()

def test_new_score(auth, client):
    """Verify that a new score can be registered."""
    username = "user1"
    password = "a"

    # Sign in
    response = auth.login(username, password)

    # Simulate player actions to start the game
    client.get("/gamepage")
    client.get("/NinerNav/game/")
    with client.session_transaction() as session:
        lat = session.get("map_lat")
        lon = session.get("map_lon")
        map_name = session.get("map_name")

    # Verify that no new score is on the leaderboards
    response = client.get("/leaderboard")
    assert f"{username} ({map_name}) - Score: 100" not in response.data.decode()

    client.post("/gamepage", data={"latitude": lat, "longitude": lon})

    # Verify that the score appears on the leaderboards
    response = client.get("/leaderboard")
    assert f"{username} ({map_name}) - Score: 100" in response.data.decode()

def test_csrf(auth, client):
    """Verify that CSRF protection works properly."""
    # Reactivate CSRF protection
    game_controller.GPSForm.Meta.csrf = True
    user_controller.LoginForm.Meta.csrf = True
    user_controller.SignupForm.Meta.csrf = True
    user_controller.SignoutForm.Meta.csrf = True

    valid_username = "user1"
    valid_new_username = "user5"

    valid_new_email = "user5@example.com"

    valid_password = "Aaaaaaaaaaaa"

    valid_lat = 30
    valid_lng = 25

    # Test authentication endpoints
    response = auth.login(valid_username, valid_password)
    assert "Hello, " not in response.data.decode()

    response = auth.signup(valid_new_username, valid_new_email, valid_password)
    assert response.status_code != 302 # I.e., no redirect occurs, so sign up failed

    # Properly sign in to test sign out
    user_controller.LoginForm.Meta.csrf = False
    auth.login(valid_username, valid_password)
    user_controller.LoginForm.Meta.csrf = True
    response = auth.signout()
    assert valid_username not in response.data.decode()

    # Test game endpoints
    response = client.post("/gamepage", data={"latitude": valid_lat, "longitude": valid_lng})
    assert "ok" != response.data.decode()
