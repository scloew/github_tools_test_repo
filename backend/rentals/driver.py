import requests
from utils import return_movie, return_all_rentals

URI_RESOURCE = 'http://127.0.0.1:5000/api/rentals/'

USER_ID = 80


if __name__ == '__main__':
    response = requests.get(f'http://127.0.0.1:5000/api/rentals/movies/{USER_ID}')
    print(response)
    print(response.status_code)
    print(response.json())
    print('\n==========\n')
    response = requests.post(f'{URI_RESOURCE}/returns/{USER_ID}')
