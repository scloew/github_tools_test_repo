import pyodbc
from datetime import datetime, timedelta

from backend.members.routes import get_member, get_member_type
from backend.cart.utils import delete_cart

conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" +
            "Server=STEVE_PC\MSSQLSERVER01;" +
            "Database=BluckBoster;" +
            "Trusted_Connection=yes"
        )
cursor = conn.cursor()


rented_to_json = lambda r: {'member_id': r.member_id, 'movie_id': r.movie_id,
                            'date_rented': r.date_rented, 'due_date': r.due_date}


def rent_movie(member_id, movie_id):
    member = get_member(member_id)[0]
    type_id = member['member_type']
    member_type = get_member_type(type_id)[0]
    rental_fee = member_type['rental_fee']

    update_inventory_and_rented(movie_id)

    insert_into_rented(member_id, movie_id, member_type)

    cursor.execute(f'UPDATE Members SET currently_rented={member["currently_rented"] + 1}, '
                   f'current_bill={rental_fee + member["current_bill"]} WHERE member_id={member_id}')

    conn.commit()


def update_inventory_and_rented(movie_id, inc_rented=1):

    cursor.execute(f'SELECT * FROM Movies WHERE movie_id={movie_id}')
    movie = cursor.fetchone()
    inventory, rented = movie.inventory, movie.rented
    if inventory <= 0 and 0 < inc_rented:
        print('\tMovie stock can never be negative')
        raise Exception('Movie stock can never be negative')
    cursor.execute(f'UPDATE Movies SET inventory={inventory - inc_rented}, rented={rented + inc_rented} '
                   f'WHERE movie_id={movie_id}')
    conn.commit()


def insert_into_rented(member_id, movie_id, member_type):

    rent_duration = member_type['rent_duration']

    today = datetime.now()
    cursor.execute(f'INSERT into RentedMovies (member_id, movie_id, date_rented, due_date)' +
                   f' VALUES(?, ?, ?, ?)', (member_id, movie_id, today, today + timedelta(days=rent_duration)))
    conn.commit()


def return_all_rentals(member_id):
    for movie_id in get_all_rented_movies(member_id):
        print(f'\tmovie_id={movie_id}')
        return_movie(member_id, movie_id)


def get_all_rented_movies(member_id):
    print(f'SELECT * FROM RentedMovies WHERE member_id={member_id}')
    cursor.execute(f'SELECT * FROM RentedMovies WHERE member_id={member_id}')
    data = cursor.fetchall()
    print(f'data[0]:={data[0]}')
    for row in data:
        print(row)
        yield row.movie_id
    # return [row.movie_id for row in data]


def return_movie(member_id, movie_id):
    cursor.execute(f'DELETE FROM RentedMovies WHERE member_id={member_id} and movie_id={movie_id}')
    member = get_member(member_id)[0]
    print(f'\tmember={member}')
    rented = member['currently_rented']
    print(f'\trented={rented}, type(rented)={type(rented)}')
    if rented <= 0:
        raise Exception(f'Rented={rented}; must be greater than 0')
    cursor.execute(f'UPDATE Members SET currently_rented={rented-1} where member_id={member_id}')
    update_inventory_and_rented(movie_id, inc_rented=-1)
    conn.commit()
