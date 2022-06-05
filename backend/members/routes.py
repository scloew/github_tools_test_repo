from flask import Blueprint, request, Response
import pyodbc

from backend.members.utils import username_exists, create_member, password_is_correct

conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};" +
            "Server=STEVE_PC\MSSQLSERVER01;" +
            "Database=BluckBoster;" +
            "Trusted_Connection=yes"
        )

members = Blueprint('Members', __name__)

member_to_json = lambda r: {'member_id': r.member_id, 'first_name': r.first_name.rstrip(),
                            'last_name': r.last_name.rstrip(), 'member_type': r.member_type,
                            'currently_rented': r.currently_rented, 'date_joined': r.date_joined,
                            'bill_due': r.bill_due, 'current_bill': r.current_bill}


@members.route('/api/member/<int:member_id>')
def get_member(member_id):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM Members WHERE member_id={member_id}')

    member = member_to_json(cursor.fetchone())
    return member, 200


@members.route('/api/member/type/<int:member_type>')
def get_member_type(member_type):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM MemberTypes WHERE member_type={member_type}')
    to_member_type_json = lambda r: {'member_type': r.member_type, 'max_rents': r.max_rents,
                                     'rent_duration': r.rent_duration, 'late_fee': r.late_fee,
                                     'rental_fee': r.rental_fee, 'monthly_fee': r.monthly_fee}
    data = cursor.fetchone()
    print(f'data=data')
    ret_json = to_member_type_json(cursor.fetchone())
    return ret_json, 200


@members.post('/api/member/register')
def register_member():
    print('Register user endpoint hit')
    data = request.json
    print(f'data={data}')
    username = data.get('username', '')
    print(f'username={username}')
    if not len(username) or username_exists(username):
        print('early out 1')
        return {304: 'username must not be empty'}
    if username_exists(username):
        print('early out 2')
        return {304: 'username is already taken. Please come up with a new one'}
    first_name, last_name, member_type, password = \
        data.get('first_name'), data.get('last_name'), data.get('member_type'), data.get('password')
    create_member(first_name, last_name, username, member_type, password)
    return {'202': f'{username} is now registered!'}


@members.post('/api/member/login')
def login():
    data = request.json
    username, password = data.get('username'), data.get('password')
    login_successful, member_id = password_is_correct(username, password)
    if login_successful is False:
        return {'message': 'Incorrect password or username'}, 404
    return {'message': 'Successful login!'}
