import requests
from utils import username_exists, create_member, password_is_correct

URI_RESOURCE = 'http://127.0.0.1:5000/api/member/'

DELIM = '\n=================\n=================\n'


if __name__ == '__main__':
    response = requests.get(f'{URI_RESOURCE}{1}')
    print(f'{URI_RESOURCE}{1}')
    print(f'respsonse={response}')
    print(response.json())
    print(DELIM)

    # print(f'{URI_RESOURCE}type/{1}')
    # response = requests.get(f'{URI_RESOURCE}type/{1}')
    # print('memberType:=', response.json())
    # print(DELIM)
    # username_exists = username_exists('marge_simpson')
    # print(username_exists)
    # create_member("Marge", "Simpson", "marge_simpson", 1, 'mmm')
    # print(DELIM)
    # print(f'testing register user endpoint')
    # response = requests.post(f'{URI_RESOURCE}register',
    #                          json={'first_name': 'Bart', 'last_name': 'Simpson',
    #                                'username': 'bart_simpson', 'member_type': 2,
    #                                'password': 'ay_caramba'})
    # print(f'response.ok={response.ok}')
    # print(f'response.json()={response.json()}')

    print(DELIM)
    print('Testing password look up')
    is_correct = password_is_correct('arnie_pye', 'lrlr')
    print(f'is_correct={is_correct}')

    print(DELIM)
    print('testing login endpoint')
    response = requests.post(f'{URI_RESOURCE}login',
                             json={'username': 'arnie_pye', 'password': 'lrlr'})
    print(f'response.ok={response.ok}, response.status={response.status_code}')
    print(f'response.json()={response.json()}')

    print(DELIM)
    print('testing login endpoint - bad username')
    response = requests.post(f'{URI_RESOURCE}login',
                             json={'username': 'bunnies', 'password': 'lrlr'})
    print(f'response.ok={response.ok}, response.status={response.status_code}')
    print(f'response.json()={response.json()}')

    print(DELIM)
    print('testing login endpoint - bad username')
    response = requests.post(f'{URI_RESOURCE}login',
                             json={'username': 'arnie_pye', 'password': 'xxxx'})
    print(f'response.ok={response.ok}, response.status={response.status_code}')
    print(f'response.json()={response.json()}')
