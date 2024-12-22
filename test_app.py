import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.test_movie = {
            'title': 'Movie Title',
            'release_year': 2020
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

        # Setup authentication tokens info
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["Casting_Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Casting_Director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive_Producer"]["jwt_token"]

        self.auth_headers = {
            "Casting_Assistant": f'Bearer {assistant_jwt}',
            "Casting_Director": f'Bearer {director_jwt}',
            "Executive_Producer": f'Bearer {producer_jwt}'
        }


    def tearDown(self):
        pass

    # GET Endpoint Tests
    # -------------------------------------------------------------------------

    # Creating a test for the /movies GET endpoint
    def test_get_movies(self):
        headers = {
            'Authorization': self.auth_headers["Casting_Assistant"]
        }
        res = self.client().get('/movies', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movies_fail(self):

        res = self.client().get('/moviess')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data.get("message"), "Resource not found")

    def test_get_actors(self):
        headers = {
            'Authorization': self.auth_headers["Casting_Assistant"]
        }
        res = self.client().get('/actors', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actors_fail(self):
        res = self.client().get('/acters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_add_movie(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        res = self.client().post('/movies/new', json=self.test_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_movie_fail(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        movie_fail = {"title": "Movie"}
        res = self.client().post(
            '/movies/new',
            json=movie_fail, headers=headers)

        self.assertEqual(res.status_code, 422)

    def test_add_actor(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }

        # check movie id is exist or not
        movie = Movie.get_all()
        if not movie:
            movie = Movie(title="Some Movie Title", release_year=2020)
            movie.insert()

        test_movie_id = movie[0].id

        test_actor = {
            'name': 'Actor Name',
            'age': 33,
            'gender': 'female',
            'movie_id': test_movie_id
        }
        res = self.client().post('/actors/new', json=test_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    def test_add_actor_fail(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        res = self.client().post('/actors/new', json={'name': 'John Doe'}, headers=headers)

        self.assertEqual(res.status_code, 422)

    def test_update_movie(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }

        # check movie id is exist or not
        movie = Movie.get_all()
        if not movie:
            movie = Movie(title="Some Movie Title", release_year=2020)
            movie.insert()

        test_movie_id = movie[0].id

        res = self.client().patch(
            f'/movies/update/{test_movie_id}',
            json={
                'title': 'Updated Movie Title'}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])

    def test_update_movie_fail(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        res = self.client().patch('/movies/update/100000000',
                                  json={'title': 'Updated Movie Title'}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_update_actor(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }

        # check movie id is exist or not
        movie = Movie.get_all()
        if not movie:
            movie = Movie(title="Some Movie Title", release_year=2020)
            movie.insert()

        test_movie_id = movie[0].id

        # check actor id is exist or not
        actor = Actor.get_all()
        if not actor:
            actor = Actor(name="Actor Name", age=33, gender="female", movie_id=test_movie_id)
            actor.insert()

        test_actor_id = actor[0].id
        
        res = self.client().patch(
            f'/actors/update/{test_actor_id}',
            json={
                'name': 'Updated Name'}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])

    def test_update_actor_fail(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        res = self.client().patch(
            '/actors/update/100000000',
            json={
                'name': 'Updated Name'}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        # check movie id is exist or not
        movie = Movie.get_all()
        if not movie:
            movie = Movie(title="Some Movie Title", release_year=2020)
            movie.insert()

        test_movie_id = movie[0].id

        # Delete actors related to  this movie
        actors = Actor.get_actors_by_movie_id(test_movie_id)
        for actor in actors:
            actor.delete()

        res = self.client().delete(f'/movies/delete/{test_movie_id}', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_movie_fail(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        res = self.client().delete('/movies/delete/100000000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_actor(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        # check movie id is exist or not
        movie = Movie.get_all()
        if not movie:
            movie = Movie(title="Some Movie Title", release_year=2020)
            movie.insert()

        test_movie_id = movie[0].id

        # check actor id is exist or not
        actor = Actor.get_all()
        if not actor:
            actor = Actor(name="Actor Name", age=33, gender="female", movie_id=test_movie_id)
            actor.insert()

        test_actor_id = actor[0].id

        res = self.client().delete(f'/actors/delete/{test_actor_id}', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_actor_fail(self):
        headers = {
            'Authorization': self.auth_headers["Executive_Producer"]
        }
        res = self.client().delete('/actors/delete/100000000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    

if __name__ == '__main__':
    unittest.main()