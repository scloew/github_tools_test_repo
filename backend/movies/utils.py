import pyodbc
from datetime import datetime, timedelta

from members.routes import get_member, get_member_type
from cart.utils import delete_cart

conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" +
            "Server=STEVE_PC\MSSQLSERVER01;" +
            "Database=BluckBoster;" +
            "Trusted_Connection=yes"
        )
cursor = conn.cursor()


movie_to_json = lambda r: {'movie_id': r.movie_id, 'title': r.title.rstrip(), 'director': r.director.rstrip(),
                           'lead': r.lead.rstrip(), 'support': r.support.rstrip(), 'rating': r.rating,
                           'year': r.year, 'inventory': r.inventory, 'rented': r.rented}


rented_to_json = lambda r: {'member_id': r.member_id, 'movie_id': r.movie_id,
                            'date_rented': r.date_rented, 'due_date': r.due_date}


def get_movie(movie_id):

    cursor.execute(f'SELECT * FROM Movies WHERE movie_id={movie_id}')
    return movie_to_json(cursor.fetchone())
