"""A set of functions to manage the state of the game and determine which page the user should be at
given their progression in the game.

This file interacts with flask's session object. The keys that may be modified by this file are
listed below.

* gamestate - the current state of the game that the user is in, one of GameState's values
* map_order - the order in which the user is going to progress through maps
* map_index - the index of the next map that the user should play
* map_lat - the latitude that the current map is located at
* map_lon - the longitude that the current map is located at
* map_name - the name of the current map
* map_score - the score the user achieved on the current map this game
* map_id - the id of the current map in the database
* map_desc - the description of the current map
* guess_lat - the latitude of the most recent guess
* guess_lon - the longitude of the most recent guess
* total_score - the cumulative score the user has accumulated this play session
* old_total_score - the cumulative score for the user's previous attempt
* games_played - the number of games a user played in a given run
* old_games_played - the number of games played in the user's previous attempt
"""
from enum import Enum
from flask import session
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms.validators import DataRequired
from typing import Dict, Any
import random
from math import radians, cos, sin, asin, sqrt, exp
from . import session as session_controller
from ..models import game as game_model, models

class GameState(Enum):
    STARTED = 0
    SUBMITTED = 1
    PROCESSED = 2
    FINISHED = 3

gameinfo: Dict[str, Any] = {}

class GPSForm(FlaskForm):
    latitude = FloatField("latitude", validators=[DataRequired()])
    longitude = FloatField("longitude", validators=[DataRequired()])

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

    if "total_score" not in session:
        session["total_score"] = 0

    if "games_played" not in session:
        session["games_played"] = 0

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
    """Sets the current user's state to the specified state.

    Args:
        state: The GameState that should be set
    """
    session["gamestate"] = state.value

def unset_state():
    """Delete the gamestate key from flask's session."""
    session.pop("gamestate")

def is_in_state(state: GameState) -> bool:
    """Determines if the user is in the specified state.

    Args:
        state: The GameState to check the actual state against

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
    """Gets the next map that the user should play and stores information about it. Also ensures
    that there is a valid next map.

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

    # Store information about the selected map
    session["map_lat"] = map.latitude
    session["map_lon"] = map.longitude
    session["map_name"] = map.name
    session["map_id"] = map.id
    session["map_desc"] = map.description

    return map

def calculate_score(form: GPSForm):
    """Calculates and stores a user's score for the game in the map_score key in the user's session
    and in the database.

    The user's session must have the correct coordinates for the current map stored. The user's
    guess is stored in the session under "guess_lat" and "guess_lng".

    Arguments:
        form: The GPSForm that the user submitted

    Returns:
        The user's score, which is an integer in the range [0, 100]
    """
    session["guess_lat"] = form.latitude.data
    session["guess_lon"] = form.longitude.data

    session["games_played"] += 1

    dist = _haversine(
        form.latitude.data,
        form.longitude.data,
        session["map_lat"],
        session["map_lon"]
    )

    # Arbitrary sigmoid function, returns non-zero value if within 52 meters of the actual location
    score = int(200 * (1 + ((-1)/(1 + exp(-dist/10)))))
    session["map_score"] = score
    session["total_score"] += score

    # Register a new score in the database if the user is authenticated
    if session_controller.is_user_authenticated():
        game_model.register_score(
            session["user_id"],
            session["map_id"],
            score
        )

def reset_run():
    """Resets the user's statistics for the run.

    Also moves the current stats into old_* keys.
    """
    session["old_total_score"] = session["total_score"]
    session["total_score"] = 0

    session["old_games_played"] = session["games_played"]
    session["games_played"] = 0

def _reset_maps():
    """Resets the map order and index for the current session. This should be called when all maps
    have been exhausted.
    """
    num_maps = gameinfo["num_maps"]
    session["map_order"] = random.sample([i+1 for i in range(num_maps)], num_maps)
    session["map_index"] = 0

def _haversine(lat1, lon1, lat2, lon2) -> float:
    """Computes the distance between two GPS coordinates using the Haversine formula.

    Based on https://stackoverflow.com/a/4913653. This approximates Earth as a perfect sphere, which
    is not mathematically perfect.

    Arguments:
        lat1: The latitude of the first point
        lon1: The longitude of the first point
        lat2: The latitude of the second point
        lon2: The longitude of the second point

    Returns:
        The distance between the two points in meters
    """
    # Convert to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Compute the difference in angles
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Apply the haversine formula (https://en.wikipedia.org/wiki/Haversine_formula)
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Scale the result by the radius of Earth in km, then convert to meters
    return c * 6371 * 1000