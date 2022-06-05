from flask import Blueprint, jsonify, Response
# TODO figure out how to do this with sql alchemy

# from backend.movies.utils import (conn, movie_to_json)
from movies.utils import (conn, movie_to_json)

movies = Blueprint('Movies', __name__)


@movies.route('/api/movies')
def view_movies():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM MOVIES')
    movies_json = map(movie_to_json, cursor.fetchall())
    return jsonify(list(movies_json))


@movies.route('/api/movies/<int:movie_id>')
def get_movie(movie_id):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM Movies WHERE movie_id={movie_id}')
    movie = movie_to_json(cursor.fetchone())
    return movie
