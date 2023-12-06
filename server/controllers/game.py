"""A set of functions to manage the state of the game and determine which page the user should be at
given their progression in the game.

This file interacts with flask's session object. The keys that may be modified by this file are
listed below.

* gamestate - the current state of the game that the user is in, one of GameState's values
* map_order - the order in which the user is going to progress through maps
* map_index - the index of the next map that the user should play
"""
from enum import Enum
from flask import session
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms.validators import DataRequired
from typing import Dict, Any
import random
from ..models import game as game_model, models

class GameState(Enum):
    STARTED = 0
    SUBMITTED = 1
    PROCESSED = 2
    FINISHED = 3

gameinfo: Dict[str, Any] = {}

def init_game_info() -> Dict[str, Any]:
    """Initializes some information about the game.

    This should be called on server start. The information this function obtains is stored in the
    global gameinfo dict. The keys set in gameinfo are listed below.

    * num_maps - the number of maps available to be played

    Returns:
        A reference to the gameinfo object
    """
    gameinfo["num_maps"] = game_model.get_map_count()

    return gameinfo

def start_game():
    """Initializes several variables for the user's game.

    Certain pages may only be accessed when the user's gamestate is a certain value, listed below.
    To make sure that repeated maps are not served, the order that the user will play the maps in is
    generated at the started and stored for the duration of the session.

    * STARTED - a game has been started, typically triggered by visiting the game prep page
    * SUBMITTED - a game has been submitted to the server but has not yet been processed
    * PROCESSED - the submitted game has been processed by the server
    * FINISHED - the user has indicated that they wish to end the game
    """
    session["gamestate"] = GameState.STARTED.value

    # Check if a map order does not exist or if all maps have been cycled through, regen if so
    if "map_order" not in session or session["map_index"] == gameinfo["num_maps"]:
        _reset_maps()

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

def get_leaderboard() -> list[tuple[str, str, int]]:
    """Gets the current global leaderboard.

    Returns:
        A list of scores, where the first entry is a username, the second is a map name, and the
        third is the score.
    """
    scores = game_model.get_top_scores()

    # Filter for just the username, map name, and score
    scores = [(s[0].username, s[1].name, s[2].score) for s in scores]

    return scores

def get_next_map() -> models.Map:
    """Gets the next map that the user should play. Also increments the map index and regenerates
    the map order if necessary.

    Returns:
        The next map that the user should play
    """
    map_index = session["map_index"]
    map = game_model.get_map_by_id(session["map_order"][map_index])
    map_index += 1

    if map_index == gameinfo["num_maps"]:
        _reset_maps()
    else:
        session["map_index"] = map_index

    return map

def _reset_maps():
    """Resets the map order and index for the current session. This should be called when all maps
    have been exhausted.
    """
    num_maps = gameinfo["num_maps"]
    session["map_order"] = random.sample([i+1 for i in range(num_maps)], num_maps)
    session["map_index"] = 0

class GPSForm(FlaskForm):
    latitude = FloatField("latitude", validators=[DataRequired()])
    longitude = FloatField("longitude", validators=[DataRequired()])