"""Contains functions for game functions, such as logging scores and getting level data."""
from sqlalchemy import desc
from .models import db, User, Map, Score
from .user import get_user_by_username

def get_user_scores(user: User|str) -> list[Score]|None:
    """Gets all of the specified user's scores.

    Args:
        user: A User object or the username of a user

    Returns:
        A list of all scores belonging to the specified user
    """
    # Ensure the user is a User
    user = _convert_user_to_obj(user)

    return Score.query.filter(Score.userid == user.id).all()

def get_user_scores_by_map(user: User|str, map: Map|str) -> list[Score]|None:
    """Gets all of the specified user's scores for a specific map.

    Args:
        user: A User object or the username of a user
        map: A Map object or the name of a map

    Returns:
        A list of all scores belonging to the specified user
    """
    # Ensure the user is a User
    user = _convert_user_to_obj(user)
    if user == None:
        return None

    # Get the map's id
    map = _convert_map_to_obj(map)
    if map == None:
        return None

    return Score.query.filter(Score.userid == user.id, Score.mapid == map.id).all()

def get_top_scores(num_scores: int=10) -> list[tuple[User, Map, Score]]:
    """Gets the top num_scores scores.

    Args:
        num_scores: The number of scores that should be retrieved
    """
    return db.session.query(User, Map, Score
        ).filter(
            User.id == Score.userid, Map.id == Score.mapid
        ).order_by(
            desc(Score.score)
        ).limit(num_scores).all()

def register_score(user: User|str, map: Map|str, score: int) -> Score:
    """Register a new score for a given user on a given map.

    Args:
        user: A User object or the username of a user
        map: A Map object or the name of a map
        score: The score that the user achieved on the given map

    Returns:
        The newly registered score
    """
    user = _convert_user_to_obj(user)
    map = _convert_map_to_obj(map)

    new_score = Score(userid=user.id, mapid=map.id, score=score)
    db.session.add(new_score)
    db.session.commit()

    return new_score

def get_map_by_name(map_name: str) -> Map|None:
    """Gets a map by its name if it exists.

    Args:
        map_name: The name of the map to fetch

    Returns:
        The map with the given name if such a map exists
        None if no map has the given name
    """
    return Map.query.filter(Map.name == map_name).first()

def _convert_user_to_obj(user: User|str) -> User|None:
    """Given either a User or a username, convert it to a User.

    Args:
        user: Either a username as a str or a User object

    Returns:
        The corresponding User object or None if no such user exists
    """
    if type(user) == str:
        return get_user_by_username(user)

    return user

def _convert_map_to_obj(map: Map|str) -> Map|None:
    """Given either a Map or a map name, convert it to a Map.

    Args:
        map: Either a map name as a str or a Map object

    Returns:
        The corresponding Map object or None if no such map exists
    """
    if type(map) == str:
        return get_map_by_name(map)

    return map