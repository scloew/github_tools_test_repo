import requests
delim = '\n===============\n'

USER_ID = 16

if __name__ == '__main__':
    print(f'http://127.0.0.1:5000/api/movies/rentals/{USER_ID}')
    response = requests.get(f'http://127.0.0.1:5000/api/movies/rentals/{USER_ID}')
    print([i['movie_id'] for i in response.json()])
    print(response)
    print(delim)
    print('TESTING RETURN')
    print(delim)
    response = requests.post(f'http://127.0.0.1:5000/api/movies/returns/{USER_ID}')
    print(response)
