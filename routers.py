from flask import Flask, request, abort, jsonify
from auth import requires_auth
from models import Actor, Movie

def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    ### check the health of the application ###
    @app.route('/', methods=['GET'])
    def check_app():
        """
        Check the health of the application.

        Returns:
            JSON response indicating the app is running.
        """
        return jsonify({
            'success': True,
            'description': 'App is running.'
        })
    
    ### Movies ###
    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def get_movies(payload):
        """
        Retrieve all movies.

        Args:
            payload (dict): Decoded JWT payload.

        Returns:
            JSON response containing a list of movies or 404 if no movies found.
        """
        movies = Movie.get_all()

        # if not movies:
        #     abort(404)

        movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies
        })
    
    @app.route('/movies/new', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload):
        """
        Create a new movie.

        Args:
            payload (dict): Decoded JWT payload.

        Returns:
            JSON response with the ID of the created movie or 422 if input is invalid.
        """
        body = request.get_json()

        title = body.get('title')
        release_year = body.get('release_year')

        # print(f"title: {title}, release_year: {release_year}")

        if not (title and release_year):
            abort(422)

        try:
            movie = Movie(title=title, release_year=release_year)
            movie.insert()

            return jsonify({
                'success': True,
                'movie_id': movie.id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        """
        Delete a movie by ID.

        Args:
            payload (dict): Decoded JWT payload.
            movie_id (int): ID of the movie to be deleted.

        Returns:
            JSON response indicating success or 404 if movie not found.
        """
        movie = Movie.get_by_id(movie_id)

        if movie:
            try:
                movie.delete()

                return jsonify({
                    'success': True,
                    'deleted': movie_id
                })
            except Exception as e:
                print(e)
                abort(422)

        else:
            abort(404)

    @app.route('/movies/update/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movie')
    def update_movie(payload, movie_id):
        """
        Update a movie by ID.

        Args:
            payload (dict): Decoded JWT payload.
            movie_id (int): ID of the movie to be updated.

        Returns:
            JSON response with the updated movie ID or 404 if not found.
        """
        movie = Movie.get_by_id(movie_id)

        if movie:
            try:
                body = request.get_json()
                title = body.get('title')
                release_year = body.get('release_year')

                if title:
                    movie.title = title
                
                if release_year:
                    movie.release_year = release_year

                movie.update()

                return jsonify({
                    'success': True,
                    'movie_id': movie.id
                })
            except Exception as e:
                print(e)
                abort(422)

        else:
            abort(404)

    ### Actors ###
    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_actors(payload):
        """
        Retrieve all actors.

        Args:
            payload (dict): Decoded JWT payload.

        Returns:
            JSON response containing a list of actors or 404 if no actors found.
        """
        actors = Actor.get_all()

        # if not actors:
        #     abort(404)

        actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors
        })
    
    @app.route('/actors/new', methods=['POST'])
    @requires_auth('create:actor')
    def add_actor(payload):
        """
        Add a new actor.

        Args:
            payload (dict): Decoded JWT payload.

        Returns:
            JSON response with the ID of the created actor or 422 if input is invalid.
        """
        body = request.get_json(force=True)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        movie_id = body.get('movie_id')

        if not (name and age and gender and movie_id):
            abort(422)

        try:
            actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
            actor.insert()

            return jsonify({
                'success': True,
                'actor_id': actor.id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actors(jwt, actor_id):
        """
        Delete an actor by ID.

        Args:
            jwt (dict): Decoded JWT payload.
            actor_id (int): ID of the actor to be deleted.

        Returns:
            JSON response indicating success or 404 if actor not found.
        """
        actor = Actor.get_by_id(actor_id)

        if actor:
            try:
                actor.delete()

                return jsonify({
                    'success': True,
                    'deleted': actor_id
                })
            except Exception as e:
                print(e)
                abort(422)
        else:
            abort(404)

    @app.route('/actors/update/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actor')
    def update_actor(payload, actor_id):
        """
        Update an actor by ID.

        Args:
            payload (dict): Decoded JWT payload.
            actor_id (int): ID of the actor to be updated.

        Returns:
            JSON response with the updated actor ID or 404 if not found.
        """
        actor = Actor.query.get(actor_id)

        if actor:
            try:
                body = request.get_json()

                name = body.get('name')
                age = body.get('age')
                gender = body.get('gender')
                movie_id = body.get('movie_id')

                if name:
                    actor.name = name
                if age:
                    actor.age = age
                if gender:
                    actor.gender = gender
                if movie_id:
                    actor.movie_id = movie_id

                actor.update()

                return jsonify({
                    'success': True,
                    'actor_id': actor.id
                })

            except Exception as e:
                print(e)
                abort(422)

        else:
            abort(404)
