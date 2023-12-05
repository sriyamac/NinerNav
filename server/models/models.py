"""Holds all the database models for the ninernav database.

This file holds models for all tables in the database. Database operations are handled elsewhere.
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Set up SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """A model for the user table.

    Attributes:
        id: The ID of the user, which serves as a primary key
        username: The username of the user
        email: The email of the user
        password: The argon2 hash of the user's password
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(77), nullable=False)

class Map(db.Model):
    """A model for the map table.

    Attributes:
        id: The ID of the map, which serves as a primary key
        name: The human-readable name of the map
        latitude: The latitude at which the map is located
        longitude: The longitude at which the map is located
        imgpath: The relative filepath to the image for the map
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)
    imgpath = db.Column(db.String(100), unique=True, nullable=False)

class Score(db.Model):
    """A model for the score table.

    Attributes:
        id: The ID of the score, which serves as a primary key
        userid: The ID of the user who acheived this score
        mapid: The ID of the map that this score was achieved on
        time: The time at which this score was achieved
    """
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    mapid = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)

def init_db(app: Flask):
    """Initialize the database connection. This must be called before any database operations are
    performed.

    Args:
        app: The Flask app
    """
    db.init_app(app)