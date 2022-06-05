import pyodbc
from random import randint
from datetime import datetime, timedelta

MAX_MEMBER_ID = 1_000_000_000

conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" +
            "Server=STEVE_PC\MSSQLSERVER01;" +
            "Database=BluckBoster;" +
            "Trusted_Connection=yes"
        )


def username_exists(name):
    cursor = conn.cursor()
    print(f"SELECT * FROM  Passwords WHERE username='{name}'")
    cursor.execute(f"SELECT * FROM  Passwords WHERE username='{name}'")
    data = cursor.fetchall()
    return 0 < len(data)


def user_exists(member_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Members where member_id='{member_id}'")


def insert_into_members(member_id, first_name, last_name, member_type):
    today = datetime.now()
    cursor = conn.cursor()
    # TODO: need to make sure member type is valid
    cursor.execute(
            'INSERT into Members(member_id, first_name, last_name, member_type, currently_rented, date_joined, bill_due, '
            'current_bill)'
            'values(?,?,?,?,?,?,?,?);',
            (member_id, first_name, last_name, member_type, 0, today, today+timedelta(days=31), 1)
    )


def create_member(first_name, last_name, username, member_type, password):
    cursor = conn.cursor()
    member_id = randint(0, MAX_MEMBER_ID)
    while user_exists(member_id):
        member_id = randint(0, MAX_MEMBER_ID)
    cursor.execute('INSERT INTO Passwords (username, password, member_id) values(?,?,?)',
                   (username, password, member_id))
    insert_into_members(member_id, first_name, last_name, member_type)
    conn.commit()


def password_is_correct(username, password):
    cursor = conn.cursor()
    print(f'SELECT password, member_id FROM Passwords WHERE username={username}')
    cursor.execute(f"SELECT password, member_id FROM Passwords WHERE username='{username}'")
    data = cursor.fetchone()
    if data is None:
        return False, None
    return data.password == password, data.member_id
