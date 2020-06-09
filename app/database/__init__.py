import contextlib
import os
import time

from flaskext.mysql import MySQL

from app.utils import server_type

BASE_SQL = os.path.join('app', 'database', 'sql')
CENTRAL_SQL = os.path.join(BASE_SQL, 'central.sql')
DATA_SQL = os.path.join(BASE_SQL, 'data.sql')


@contextlib.contextmanager
def cursor():
    con = mysql.connect()
    cursor = con.cursor()
    try:
        yield cursor
    finally:
        cursor.close()
        con.commit()
        con.close()


def init_mysql(app):
    # globally set mysql variable
    globals()['mysql'] = MySQL(app)
    time.sleep(30) # needs some time apparently
    if server_type() == 'CENTRAL':
        sql_file = CENTRAL_SQL
    elif server_type() == 'DATA':
        sql_file = DATA_SQL
    with cursor() as cur:
        with open(sql_file, 'r') as f:
            cur.execute(f.read())


def test_db():
    with cursor() as cur:
        cur.execute("INSERT INTO test VALUES (1)")

