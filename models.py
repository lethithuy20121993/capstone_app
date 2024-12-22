"""
Database Models and Setup for a Flask Application

This module defines the database models and setup for a Flask application using SQLAlchemy. It includes classes for `Movie` and `Actor` 
and their respective relationships and operations. Additionally, it provides functions to initialize and set up the database.

Modules:
    os: Provides access to environment variables.
    sqlalchemy: Used for defining database models and operations.
    flask_sqlalchemy: Provides SQLAlchemy integration with Flask.
    settings: Contains application settings, including `DATABASE_URL`.

Classes:
    Movie: Represents a movie record in the database.
    Actor: Represents an actor record in the database.

Functions:
    setup_db(app): Configures and initializes the database for the Flask application.
    create_tables(): Creates all database tables based on defined models.

"""
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from settings import DATABASE_URL

db = SQLAlchemy()

def setup_db(app):
    """
    Sets up the database for the Flask application.

    Configures the database URI and disables SQLAlchemy track modifications to enhance performance.
    Binds the SQLAlchemy object to the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def create_tables():
    """
    Creates all database tables based on the defined models.

    This function should be called after the application has been initialized and
    the database models are defined.
    """
    db.create_all()

class Movie(db.Model):
    """
    Represents the `movies` table in the database.

    Attributes:
        id (int): Primary key of the movie.
        title (str): Title of the movie.
        release_year (int): Release year of the movie.
        actors (relationship): Relationship to the `Actor` model.

    Methods:
        insert(): Adds the current instance to the database.
        update(): Commits changes for the current instance to the database.
        delete(): Removes the current instance from the database.
        format(): Returns a dictionary representation of the movie.
        get_by_id(record_id): Retrieves a movie by its ID.
        get_all(): Retrieves all movies from the database.
    """
    __tablename__ = 'movies'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    release_year = Column(Integer())
    actors = db.relationship('Actor', backref='movies')

    def insert(self):
        """
        Adds the current movie instance to the database and commits the transaction.
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Commits changes for the current movie instance to the database.
        """
        db.session.commit()

    def delete(self):
        """
        Removes the current movie instance from the database and commits the transaction.
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        Returns a dictionary representation of the movie instance.

        Returns:
            dict: A dictionary containing the movie's id, title, and release year.
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }

    @classmethod
    def get_by_id(cls, record_id):
        """
        Retrieves a movie record from the database by its ID.

        Args:
            record_id (int): The ID of the movie to retrieve.

        Returns:
            Movie: The movie instance if found, or None if not found.
        """
        return db.session.query(cls).get(record_id)

    @classmethod
    def get_all(cls):
        """
        Retrieves all movie records from the database.

        Returns:
            list: A list of all movie instances.
        """
        return db.session.query(cls).all()

class Actor(db.Model):
    """
    Represents the `actors` table in the database.

    Attributes:
        id (int): Primary key of the actor.
        name (str): Name of the actor.
        age (int): Age of the actor.
        gender (str): Gender of the actor.
        movie_id (int): Foreign key referencing the `movies` table.

    Methods:
        insert(): Adds the current instance to the database.
        update(): Commits changes for the current instance to the database.
        delete(): Removes the current instance from the database.
        format(): Returns a dictionary representation of the actor.
        get_by_id(record_id): Retrieves an actor by its ID.
        get_all(): Retrieves all actors from the database.
    """
    __tablename__ = 'actors'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    age = Column(Integer())
    gender = Column(String())

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'),
        nullable=False
    )

    def insert(self):
        """
        Adds the current actor instance to the database and commits the transaction.
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Commits changes for the current actor instance to the database.
        """
        db.session.commit()

    def delete(self):
        """
        Removes the current actor instance from the database and commits the transaction.
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        Returns a dictionary representation of the actor instance.

        Returns:
            dict: A dictionary containing the actor's id, name, age, gender, and movie_id.
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }

    @classmethod
    def get_by_id(cls, record_id):
        """
        Retrieves an actor record from the database by its ID.

        Args:
            record_id (int): The ID of the actor to retrieve.

        Returns:
            Actor: The actor instance if found, or None if not found.
        """
        return db.session.query(cls).get(record_id)

    @classmethod
    def get_all(cls):
        """
        Retrieves all actor records from the database.

        Returns:
            list: A list of all actor instances.
        """
        return db.session.query(cls).all()
    
    @classmethod
    def get_actors_by_movie_id(cls, movie_id):
        """
        Retrieves all actor records from the database by movie_id.

        Args:
            movie_id (int): The ID of the movie to filter actors by.

        Returns:
            list: A list of Actor instances associated with the given movie_id.
        """
        return db.session.query(cls).filter(cls.movie_id == movie_id).all()
