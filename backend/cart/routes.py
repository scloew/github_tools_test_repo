from flask import Blueprint, jsonify, request, Response
import json
# TODO figure out how to do this with sql alchemy
import pyodbc

from backend.cart.utils import conn, cursor, get_cart, delete_cart
from backend.movies.routes import get_movie
from backend.rentals.utils import rent_movie

cart = Blueprint('Cart', __name__)


@cart.route('/api/cart/add/', methods=['POST'])
def add_to_cart():
    data = json.loads(request.data)
    print(f'\t add data={data}')
    member_id = data['member_id']
    movie_id = data['movie_id']

    cursor.execute('INSERT INTO CARTS(member_id, movie_id)'
                   'VALUES(?,?)',
                   (member_id,
                    movie_id)
                   )
    conn.commit()

    return {'status': 'success'}, 204


@cart.route('/api/cart/remove/', methods=['POST'])
def remove_from_cart():
    data = json.loads(request.data)
    print(f'\tdata={data}')
    member_id = data['member_id']
    movie_id = data['movie_id']

    cursor.execute(f'DELETE from CARTS where (member_id={member_id}) AND (movie_id={movie_id})')
    conn.commit()

    return {'status': 'success'}, 202


@cart.route('/api/cart/<int:id>')
def fetch_cart(id):
    movies = get_cart(id)
    return jsonify(movies), 200


@cart.route('/api/cart/movies')
def get_movies_in_cart():
    movie_ids = request.args['movies'].split(',')
    movies = [get_movie(movie_id) for movie_id in movie_ids]
    return jsonify(movies)


@cart.route('/api/cart/checkout/', methods=['POST'])
def checkout():
    args = json.loads(request.data)

    member_id = args['member_id']
    movies = get_cart(member_id)

    for movie in movies:
        rent_movie(member_id, movie)

    delete_cart(member_id)

    return Response(status=202)
