import requests

from routes import *

DELIM = '\n=========\n'
URI_RESOURCE = 'http://127.0.0.1:5000/api/cart/'
USER_ID = 16

if __name__ == '__main__':
    # print(requests.get('http://127.0.0.1:5000/api/cart/movies', json={'movies': get_cart(16)}))
    # response = requests.post('http://127.0.0.1:5000/api/cart/checkout', json={'member_id': 48})
    response = requests.get(f'{URI_RESOURCE}{USER_ID}')
    print(f'cart={response.json()}')
    print(f'{URI_RESOURCE}remove/')
    response = requests.post(f'http://127.0.0.1:5000/api/cart/remove/', json={'member_id': 96, 'movie_id': 5})
    print(response, response.ok)
    print(response.json())

