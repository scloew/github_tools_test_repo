from flask import (Blueprint, jsonify, Response, request)

from backend.movies.utils import get_movie
from backend.rentals.utils import (conn, rented_to_json, return_all_rentals, return_movie)

rentals = Blueprint('rentals', __name__)


@rentals.route('/api/rentals/<int:member_id>')
def get_rented_movies(member_id):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM RentedMovies WHERE member_id={member_id}')
    rented_movies = map(rented_to_json, cursor.fetchall())
    return jsonify(list(rented_movies))


@rentals.route('/api/rentals/returns/<int:member_id>', methods=['POST'])
def return_all_rented_movies(member_id):
    return_all_rentals(member_id)
    return Response(status=202)


@rentals.post('/api/rentals/return/<int:member_id>/<int:movie_id>')
def return_rental(member_id, movie_id):
    print(f'returning for member: {member_id} movie: {movie_id}')
    return_movie(member_id, movie_id)
    return Response(status=202)


@rentals.route('/api/rentals/movies/<int:member_id>')
def get_rented_movies_info(member_id):
    rented_movies = get_rented_movies(member_id).json
    movies = [{**get_movie(movie['movie_id']), **movie} for movie in rented_movies]
    return jsonify(movies)
