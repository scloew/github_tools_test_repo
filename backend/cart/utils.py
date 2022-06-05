import pyodbc


conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" +
            "Server=STEVE_PC\MSSQLSERVER01;" +
            "Database=BluckBoster;" +
            "Trusted_Connection=yes"
        )
cursor = conn.cursor()


def get_cart(member_id):
    cursor.execute(f'SELECT movie_id FROM Carts WHERE member_id={member_id}')

    movies = [row.movie_id for row in cursor.fetchall()]
    return movies


def delete_cart(member_id):
    cursor.execute(f'DELETE FROM Carts WHERE member_id={member_id}')
    conn.commit()


def remove_movie_from_cart(member_id, movie_id):
    cursor.execute(f'DELETE FROM Carts WHERE member_id={member_id} AND movie_id={movie_id}')
    conn.commit()
