"""
Application Factory and Configuration for a Flask Application

This module defines the application factory and configuration for a Flask application. It integrates the database, CORS, 
routes, and error handlers. The application is set up using a factory pattern to allow for flexibility and easier testing.

Modules:
    os: Provides access to environment variables.
    flask: Provides the core functionality for the Flask application.
    flask_sqlalchemy: Provides SQLAlchemy integration for database operations.
    flask_cors: Enables Cross-Origin Resource Sharing (CORS) for the application.
    routers: Contains the application's route definitions.
    error_handlers: Contains custom error handler registrations.
    settings: Includes configuration values, such as `DATABASE_URL`.
    models: Defines database setup and initialization.

Functions:
    create_app(test_config=None): Creates and configures the Flask application.

Attributes:
    APP (Flask): The initialized Flask application instance.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routers import register_routes
from error_handlers import register_error_handlers
from settings import DATABASE_URL
from models import setup_db, create_tables

db = SQLAlchemy()

def create_app(test_config=None):
    """
    Creates and configures the Flask application.

    This function initializes the Flask application, configures the database, sets up CORS,
    registers routes, and error handlers.

    Args:
        test_config (dict, optional): Configuration overrides for testing. Defaults to None.

    Returns:
        Flask: The initialized Flask application instance.
    """
    # Create and configure the application
    app = Flask(__name__)
    
    # Enable CORS (Cross-Origin Resource Sharing)
    CORS(app, resources={r'/api/': {'origins': '*'}})

    # Set up the database and create tables
    setup_db(app)
    create_tables()

    # Register the routes
    register_routes(app)
    
    # Register custom error handlers
    register_error_handlers(app)
    
    return app

# Initialize the application
app = create_app()

if __name__ == '__main__':
    """
    Runs the Flask application.

    The application is started on host `0.0.0.0` and port `3000` in debug mode.
    """
    app.run(host='0.0.0.0', port=3000, debug=True)
