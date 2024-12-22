# Casting Agency Capstone Project

This is my final capstone project for Udacity's FullStack Web Developer Nanodegree.
The Casting Agency Project models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Project Dependencies

- **Flask** - Slim Python web library.
- **SQLAlchemy** - Python ORM library.
- **Render** - platform for easy hosting of web apps.
- **Postman** - API testing tool.

## Running Locally

1. Clone the project to the directory of your choice.
2. Create a virtual environment in the project directory.
3. run `pip install -r requirements.txt` to install project dependencies
4. Database setup
With Postgres running:
create database has name is `mydb`
5. Add `DATABASE_URL`, `AUTH0_DOMAIN`, `API_IDENTIFIER`, `ALGORITHMS`, `JWT_SECRET`, `AUTH0_CLIENT_ID` to the environment variables of your system.  
   On Unix systems, use:
   ```bash
   export DATABASE_URL={username}:{password}@{host}:{port}/{database_name}
   ...
   ```
   in this project, to make the environment, please run  `source setup.sh` first
5. run server with `source run_app.sh`
6. Running test:
`python test_app.py`

## Auth0 Setup
All information about Auth0 saved in `setup.sh` file to export the environment variables

### Roles
Create three roles for users under Users & Roles section in Auth0
1. Casting Assistant
- Can view actors and movies

2. Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

3. Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

### Permissions
- view:actors
- view:movies
- delete:actor
- create:actor
- edit:actor
- edit:movie
- create:movie
- delete:movie

### Set JWT Tokens in auth_config.json
Use the following link to create users and sign them in, with this way, we will generate JWT tockens
```bash
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

Note: `auth_config.json` using for running `test_app.py`
Beside, we will use `Postman` for API testing tool.

## API Documentation
### Models
1. Movie
- title
- release_date

2. Actor
- name
- age
- gender

### Endpoints

1. GET /movies
- Get all movies
- Require view:movies permission
- Example Request: curl 'http://localhost:5000/movies'
- Expected Result:
```bash
{
    "movies": [
        {
            "id": 1,
            "release_year": 2012,
            "title": "The Mask"
        },
        {
            "id": 2,
            "release_year": 2024,
            "title": "Some Movie"
        }
    ],
    "success": true
}
```

2. GET /actors
- Get all actors
- Requires view:actors permission
- Example Request: curl 'http://localhost:5000/actors'
- Expected Result:
```bash
{
    "actors": [
        {
            "age": 21,
            "gender": "Female",
            "id": 4,
            "movie_id": 1,
            "name": "Asamoah"
        }
    ],
    "success": true
}
```

3. POST /movies/new
- Creates a new movie.
- Requires post:movies permission
- Requires the title and release date.
- Example Request: (Create)
```bash
curl --location --request POST 'http://localhost:5000/movies/new' \
	--header 'Content-Type: application/json' \
	--data-raw '{
    	"title": "Some Movie",
    	"release_year": 2024
	}'
```
- Example Response:
```bash
{
    "movie_id": 2,
    "success": true
}
```

4. POST /actors/new
- Creates a new actor.
- Requires post:actors permission
- Requires the name, age and gender of the actor.
- Example Request: (Create)
```bash
curl --location --request POST 'http://localhost:5000/actors/new' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"name": "Asamoah",
		"age": "45",
		"gender": "Female",
		"movie_id": 1
    }'
```

- Example Response:
```bash
{
    "actor_id": 4,
    "success": true
}
```

5. DELETE /movies/delete/int:movie_id
- Deletes the movie with given id
- Require delete:movies permission
- Example Request: curl --request DELETE 'http://localhost:5000/movies/delete/1'
- Example Response:
```bash
{
	"deleted": 1,
	"success": true
}
```

6. DELETE /actors/delete/int:actor_id
- Deletes the actor with given id
- Require delete:actors permission
- Example Request: curl --request DELETE 'http://localhost:5000/actors/delete/1'
- Example Response:
```bash
{
	"deleted": 1,
	"success": true
}
```

7. PATCH /movies/update/<movie_id>
- Updates the movie where <movie_id> is the existing movie id
- Require update:movies permission
- Responds with a 404 error if <movie_id> is not found
- Update the corresponding fields for Movie with id <movie_id>
- Example Request:
```bash
 curl --location --request PATCH 'http://localhost:5000/movies/update/1' \
 	--header 'Content-Type: application/json' \
 	--data-raw '{
    	"title": "titanic"
	}'
```

- Example Response:
```bash
{
    "movie_id": 1,
    "success": true
}
```

8. PATCH /actors/update/<actor_id>
- Updates the actor where <actor_id> is the existing actor id
- Require update:actors
- Responds with a 404 error if <actor_id> is not found
- Update the given fields for Actor with id <actor_id>
- Example Request:
```bash
 curl --location --request PATCH 'http://localhost:5000/actors/update/1' \
 	--header 'Content-Type: application/json' \
 	--data-raw '{
 		"name": "Tom"
     }'
```

- Example Response:
```bash
{
    "actor_id": 1,
    "success": true
}
```

### Error Handling
- Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

Error types:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error

## Live API Access
The API for this project is hosted live and can be accessed at the following URL:
```bash
https://capstone-app-deployment-bmec.onrender.com
```
This API requires authentication, so please follow the instructions in the Auth0 Setup section to set up authentication tokens.

## Testing Endpoints
You can test the endpoints by using tools like Postman or curl. Ensure that you are authenticated and have the appropriate roles and permissions to test the endpoints.