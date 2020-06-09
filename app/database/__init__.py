"""The functions and classes for interaction with the database, MySQL.

Note:
    Currently the database and web server are started at the same time. This
    creates problems with a not initialized database, so there is a sleep time
    of 30 seconds before a connection with the database is attempted to be
    created.

The database should first be initialized, using the `init_mysql` function. This
call will create global variables:
    `mysql`
    `user` (`TableLoader` instance)
    `friends` (`TableLoader` instance)
    `profiles` (`TableLoader` instance)

The variables `friends` and `profiles` are only created in case the central
server is used. `user` is a table according to respectively the data or central
server SQL table configurations.

`TableLoader` instances are safe ways to interact with the respective bound
table. Data can be exported, inserted and deleted from the table. See the
documentation on the `TableLoader` class and functions.

To make more complicated database executions, the `cursor()` can be used to
interact directly with the database.
>>> with cursor() as cur:
>>>     cur.execute('my execution')
"""
import contextlib
import os
import time
import typing

from flaskext.mysql import MySQL

from app.utils import server_type, percent_type

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


class TableLoader:
    """

    """
    def __init__(self, table: str):
        self._table = table

    def export_one(self, *args, **kwargs) -> typing.Union[str, int]:
        """Export a single entry from the table.

        Note:
            By default the first result from a search in the table is returned.
            In the case where there is only one matching row, this is not a
            problem, but in the case of multiple matching rows, the row with the
            lowest `rowid`, the primary key, is returned. This is usually the row
            that was created the earliest.

        Example:
            Example calls are assuming an instance for table `user` for the
            central server.

            Export the username and address for the first row in the table:
            >>> user.export_one('username', 'address')
            ('testuser', '100 Davin Road')

            Export the address for a certain username:
            >>> user.export_one('address', username='testuser')
            '100 Davin Road'

        Args:
            args: The values (str) to be exported from the table.
            kwargs: Other options while exporting the data, see the options for
            funcion `export`.

        Returns:
            The one returned value from the table.
        """
        kwargs['limit'] = 1
        r = export(*args, **kwargs)[0]
        if len(args) == 1:
            return r[0]
        return r

    def export(self, *args, order: str='rowid', order_direction: str='desc',
               limit: int=None, **kwargs):
        """Export one or more entries from the table.

        Note:
            By default the order in which the results are returned is descending
            over the primary key, `rowid`, in the table.

        Example:
            Example calls are assuming an instance for table `user` for the
            central server.

            Export all usernames and addresses:
            >>> user.export('username', 'address')
            [
                ('testuser1', '100 Davin Road'),
                ('testuser3', '100 Davin Road'),
                ('testuser2', 'The Internet'),
                ('another user', '20 Another Road')
            ]

            Export all usernames and addresses ordered by username:
            >>> user.export('username', 'address', order='username',
                            order_direction='desc')
            [
                ('another user', '20 Another Road'),
                ('testuser1', '100 Davin Road'),
                ('testuser2', 'The Internet')
            ]

            Export the first two usernames and addresses ordered by username:
            >>> user.export('username', 'address', order='username',
                            order_direction='desc', limit=2)
            [
                ('another user', '20 Another Road'),
                ('testuser1', '100 Davin Road')
            ]

            Export all usernames living on the same address, 100 Davin Road,
            ordered by username descending:
            >>> user.export('username', order='username',
                            order_direction='desc', address='100 Davin Road')
            [
                ('testuser1', '100 Davin Road'),
                ('testuser3', '100 Davin Road')
            ]

        Args:
            args: The values (str) to be exported from the table.
            order (str): The key to order the results with.
            order_direction (str): The direction in which to order. Can have
                values 'desc' or 'asc'
            limit (int): The number of results to return.
            kwargs: The keys (str) and values (str, int) the rows should match.
        """
        with cursor() as cur:
            cur.execute(
                'SELECT ' + ','.join(args) +
                ' FROM ' + self._table +
                (
                    ' WHERE ' + ','.join(
                        '{}={}'.format(d[0], percent_type(d[1]))
                        for d in kwargs.items()
                    )
                    if len(kwargs) > 0 else
                    ''
                ) +
                ' ORDER BY {} {}'.format(order.lower(), order_direction.lower()) +
                (
                    ' LIMIT ' + str(limit)
                    if limit is not None else
                    ''
                ),
                tuple(kwargs.values())
            )
            return [
                d if len(d) > 1 else d[0]
                for d in cur.fetchall()
            ]

    def insert(self, **kwargs):
        """Insert data into the table in the database.

        Args:
            kwargs: Every variable that needs to be set in the database for the
            table. For the data server the keys that can be added can be found
            in SQL file `app/database/sql/data.sql`, and the central server
            these can be found in `app/database/sql/central.sql`.

            Note that all keys in the SQL files containing `NOT NULL` and not a
            `DEFAULT` value are requiered to be set. Others can be left empty.

            The primary key `rowid` of the table should not be set. This is the
            index of the row in the table itself and has on meaningful value
            outside of the SQL database.

            All keys that have a `DEFAULT CURRENT_TIMESTAMP` should not be
            manually set. These are set automatically, just like the `rowid` key.

        Returns:
            The return value of the database execution.
        """
        with cursor() as cur:
            return cur.execute(
                'INSERT INTO {}({})'
                    .format(self._table, ','.join(kwargs.keys())) +
                ' VALUES ({})'.format(','.join([
                    percent_type(d) for d in kwargs.values()
                ])),
                tuple(kwargs.values())
            )

    def delete(self, **kwargs):
        """Delete a row from the table in the database.

        Note:
            Any removed data cannot be recovered.

        Args:
            kwargs: The keys (str) and values (str, int) the to be deleted rows
            should match.

        Returns:
            The return value fo the database execution.
        """
        with cursor() as cur:
            return cur.execute(
                'DELETE FROM ' + self._table +
                ' WHERE ' + ','.join(
                    '{}={}'.format(d[0], percent_type(d[1]))
                    for d in kwargs.items()
                ),
                tuple(kwargs.values())
            )


def init_mysql(app):
    # globally set mysql variable
    globals()['mysql'] = MySQL(app)
    time.sleep(30) # needs some time apparently
    if server_type() == 'CENTRAL':
        sql_file = CENTRAL_SQL
        globals()['users'] = TableLoader('users')
    elif server_type() == 'DATA':
        sql_file = DATA_SQL
        globals()['users'] = TableLoader('users')
        #globals()['friends'] = TableLoader('friends')
        #globals()['profiles'] = TableLoader('profiles')
    with cursor() as cur:
        with open(sql_file, 'r') as f:
            cur.execute(f.read())


def test_db():
    with cursor() as cur:
        cur.execute("INSERT INTO test VALUES (1)")

