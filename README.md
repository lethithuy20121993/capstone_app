# Casting Agency Capstone Project

This is my final capstone project for Udacity's FullStack Web Developer Nanodegree.
The Casting Agency Project models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Project Dependencies

- **Flask** - Slim Python web library.
- **SQLAlchemy** - Python ORM library.
- **Heroku** - PaaS platform for easy hosting of web apps.
- **Postman** - API testing tool.

## Installation Instructions

1. Clone the project to the directory of your choice.
2. Create a virtual environment in the project directory.
3. run `pip install -r requirements.txt` to install project dependencies
4. Add `DATABASE_URL`, `AUTH0_DOMAIN`, `API_IDENTIFIER`, `ALGORITHMS`, `JWT_SECRET`, `AUTH0_CLIENT_ID` to the environment variables of your system.  
   On Unix systems, use:
   ```bash
   export DATABASE_URL={username}:{password}@{host}:{port}/{database_name}
   ...
   ```
   in this project, to make the environment, please run  `source setup.sh` first
5. run server with `source run_app.sh`

#### Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

## Roles
1. Casting Assistant
- GET /actors and /movies

2. Casting Director
- GET /actors and /movies
- ADD /actors and DELETE /actors
- PATCH /actors and /movies

3. Executive Producer
- GET /actors and /movies
- ADD /actors and DELETE /actors
- PATCH /actors and /movies
- ADD /movies and DELETE /movies

## JWT Tokens for each role:
1. Casting Assistant

2. Casting Director

3. Executive Producer

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