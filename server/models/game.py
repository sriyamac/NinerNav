"""Contains functions for game functions, such as logging scores and getting level data."""
from sqlalchemy import desc
from .models import db, User, Map, Score
from .user import get_user_by_username

def get_user_scores(user: User|str|int) -> list[Score]|None:
    """Gets all of the specified user's scores.

    Args:
        user: A User object, the username of a user, or a user's id

    Returns:
        A list of all scores belonging to the specified user
    """
    # Ensure the user is a User
    user_id = _convert_user_to_id(user)

    return Score.query.filter(Score.userid == user_id).all()

def get_user_scores_by_map(user: User|str|int, map: Map|str|int) -> list[Score]|None:
    """Gets all of the specified user's scores for a specific map.

    Args:
        user: A User object, the username of a user, or a user's id
        map: A Map object, the name of a map, or a map's id

    Returns:
        A list of all scores belonging to the specified user
    """
    # Ensure the user is a User
    user_id = _convert_user_to_id(user)
    if user == None:
        return None

    # Get the map's id
    map_id = _convert_map_to_obj(map)
    if map_id == None:
        return None

    return Score.query.filter(Score.userid == user_id, Score.mapid == map_id).all()

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

def register_score(user: User|str|int, map: Map|str|int, score: int) -> Score:
    """Register a new score for a given user on a given map.

    Args:
        user: A User object, the username of a user, or a user's id
        map: A Map object or the name of a map
        score: The score that the user achieved on the given map

    Returns:
        The newly registered score
    """
    user_id = _convert_user_to_id(user)
    map_id = _convert_map_to_obj(map)

    new_score = Score(userid=user_id, mapid=map_id, score=score)
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

def get_map_by_id(map_id: int) -> Map|None:
    """Gets a map by its id if it exists.

    Args:
        map_id: The id of the map to fetch

    Returns:
        The map with the given id if such a map exists
        None if no map has the given id
    """
    return Map.query.filter(Map.id == map_id).first()

def get_map_count() -> int:
    return Map.query.count()

def _convert_user_to_id(user: User|str|int) -> int|None:
    """Given either a User or a username, convert it to a User.

    Args:
        user: A User object, the username of a user, or a user's id

    Returns:
        The corresponding user id or None if no such user exists
    """
    if type(user) == str:
        user = get_user_by_username(user)
        if user != None:
            return user.id
    elif type(user) == User:
        return user.id

    return user

def _convert_map_to_obj(map: Map|str|int) -> Map|None:
    """Given either a Map or a map name, convert it to a Map.

    Args:
        map: A Map object, the name of a map, or a map's id

    Returns:
        The corresponding Map object or None if no such map exists
    """
    if type(map) == str:
        map = get_map_by_name(map)
        if map != None:
            return map.id
    elif type(map) == Map:
        return map.id

    return map