import requests


URI_RESOURCE = 'http://127.0.0.1:5000/api/movies/'
CART_URI = 'http://127.0.0.1:5000/api/movies/cart/'

DELIM = '\n=================\n=================\n'


if __name__ == '__main__':
    response = requests.get(f'{CART_URI}{1}')
    print(response)
    print(DELIM)
    response = requests.post(URI_RESOURCE+'remove-from-cart', json={'member_id': 1, 'movie_id': 5})
    print(response)
    print(DELIM)
    url = f'{URI_RESOURCE}{5}'
    print(f'\turl={url}')
    response = requests.get(url)
    print(f'response={response}')
    print(f'response.json()={response.json()}')
    print(DELIM)
    print('TESTING GETTING MOVIES IN CART')
    response = requests.get(URI_RESOURCE+f'get-movies-in-cart/{1}')
    print(f'response={response}')
    print(f'response.json()={response.json()}')

