"""A set of functions to manage the state of the game and determine which page the user should be at
given their progression in the game.

As the user advances through the game, their state should also progress. Certain pages may only be
accessed when the user's state is at a certain value. The state should be stored in flask's session
under the "gamestate" key. Those values are enumerated below.

* STARTED - a game has been started, typically triggered by visiting the game prep page
* SUBMITTED - a game has been submitted to the server but has not yet been processed
* PROCESSED - the submitted game has been processed by the server
* FINISHED - the user has indicated that they wish to end the game
"""
from enum import Enum
from flask import session
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms.validators import DataRequired

class GameState(Enum):
    STARTED = 0
    SUBMITTED = 1
    PROCESSED = 2
    FINISHED = 3

def start_game():
    """Initializes the gamestate key in flask's session to STARTED."""
    session["gamestate"] = GameState.STARTED.value

def next_state():
    """Moves the current value of gamestate to the next possible GameState.

    If no state is set, this function instead sets it to STARTED. If the state is FINISHED, the
    state is set to STARTED.
    """
    if "gamestate" not in session:
        session["gamestate"] = GameState.STARTED.value
        return

    session["gamestate"] = (session["gamestate"] + 1) % len(GameState)

def set_state(state: GameState):
    """Sets the current user's state to the specified state."""
    session["gamestate"] = state.value

def unset_state():
    """Delete the gamestate key from flask's session."""
    session.pop("gamestate")

def is_in_state(state: GameState) -> bool:
    """Determines if the user is in the specified state.

    Returns:
        False if state is not a valid GameState
        False if the current state does not match the given state
        True if the current state does match the given state
    """
    if "gamestate" not in session:
        return False
    return session["gamestate"] == state.value

class GPSForm(FlaskForm):
    latitude = FloatField("latitude", validators=[DataRequired()])
    longitude = FloatField("longitude", validators=[DataRequired()])