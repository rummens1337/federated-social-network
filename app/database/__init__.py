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
import itertools
import os
import re
import time
import typing

from flaskext.mysql import MySQL

from app.type import get_server_type, ServerType
from app.utils import percent_type

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


def where(data: dict, equal: str='=', delimiter: str=' AND ') -> str:
    return delimiter.join(
        '{} {} %s'.format(d, equal)
        for d in data.keys()
    )


class TableLoader:
    """

    """
    def __init__(self, table: str, primary_key: str):
        self._table = table
        self._primary_key = primary_key

    def exists(self, *args, **kwargs):
        pass

    def export_one(self, *args, **kwargs) -> typing.Union[str, int]:
        """Export a single entry from the table.

        Note:
            By default the first result from a search in the table is returned.
            In the case where there is only one matching row, this is not a
            problem, but in the case of multiple matching rows, the row with the
            lowest `id`, the primary key, is returned. This is usually the row
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
        return self.export(*args, **kwargs)[0]

    def export(self, *args, order: str=None, order_direction: str='desc',
               limit: int=None, as_dict: bool=False, like_prefix: bool=False,
               like_suffix: bool=False, **kwargs):
        """Export one or more entries from the table.

        Note:
            By default the order in which the results are returned is descending
            over the primary key, `id`, in the table.

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

            Export all usernames:
            >>> user.export('username', 'address')
            [
                'testuser1',
                'testuser3',
                'testuser2',
                'another user'
            ]

            Export all usernames and addresses ordered by username:
            >>> user.export('username', 'address', order='username',
                            order_direction='desc')
            [
                ('another user', '20 Another Road'),
                ('testuser1', '100 Davin Road'),
                ('testuser2', 'The Internet'),
                ('testuser3', '100 Davin Road')
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
            >>> user.export('username', 'address', order='username',
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
        if len(args) == 0:
            args = ('*',)
        order = order or self._primary_key
        with cursor() as cur:
            cur.execute(
                'SELECT ' + ','.join(args) +
                ' FROM ' + self._table +
                (
                    (
                        ' WHERE ' + where(
                            kwargs,
                            equal=(
                                '='
                                if not (like_prefix or like_suffix) else
                                'LIKE'
                            )
                        )
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
                tuple(
                    (
                        ('%' if like_prefix else '') +
                        value +
                        ('%' if like_suffix else '')
                    )
                    if type(value) is str else
                    value
                    for value in kwargs.values()
                )
            )
            result = cur.fetchall()
            if as_dict:
                description = tuple(d[0] for d in cur.description)
                return tuple(
                    dict(zip(description, d)) for d in result
                )
            return tuple(
                d if len(d) > 1 else d[0]
                for d in result
            )

    def insert(self, lastrowid=True, **kwargs):
        """Insert data into the table in the database.

        Args:
            lastrowid (bool): Return last rowid or not, default is True. See
            https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-lastrowid.html
            for more information.

            kwargs: Every variable that needs to be set in the database for the
            table. For the data server the keys that can be added can be found
            in SQL file `app/database/sql/data.sql`, and the central server
            these can be found in `app/database/sql/central.sql`.

            Note that all keys in the SQL files containing `NOT NULL` and not a
            `DEFAULT` value are requiered to be set. Others can be left empty.

            The primary key `id` of the table should not be set. This is the
            index of the row in the table itself and has on meaningful value
            outside of the SQL database.

            All keys that have a `DEFAULT CURRENT_TIMESTAMP` should not be
            manually set. These are set automatically, just like the `id` key.

        Returns:
            The rowid of the newly created row in the table, or the return value
            of the execute function if returning the last rowid is disabled.
        """
        with cursor() as cur:
            r = cur.execute(
                'INSERT INTO {}({})'
                    .format(self._table, ','.join(kwargs.keys())) +
                ' VALUES ({})'.format(','.join([
                    percent_type(d) for d in kwargs.values()
                ])),
                tuple(kwargs.values())
            )
            if not lastrowid:
                return r
            return cur.lastrowid

    def update(self, update: dict, **kwargs):
        """Update a row in a table.

        Note:
            The formatting of the variables in this function is suboptimal and
            might be changed later on. This is what it is for now.

        Example:
            Example calls are assuming an instance for table `user` for the
            central server.

            Change the address of a user with certain username. We check if the
            user exists first, then confirm the change has been made (as
            example):
            >>> user.exists(username='testuser1', address='100 Davin Road')
            True
            >>> user.update({'address': 'My New Address'}, username='testuser1')
            >>> user.exists(username='testuser1', address='100 Davin Road')
            False
            >>> user.exists(username='testuser1', address='My New Address')
            True

        Args:
            update (dict): The dictionary of keys (str) and values (str, int)
            of the changes that need to made to the selected row.
            kwargs: The keys (str) and values (str, int) for the rows for which
            the variables need to be updated with the data in dictionary update.
        """
        with cursor() as cur:
            return cur.execute(
                'UPDATE ' + self._table +
                ' SET ' + where(update, ', ') +
                ' WHERE ' + where(kwargs),
                tuple(itertools.chain(update.values(), kwargs.values()))
            )

    def exists(self, **kwargs):
        """Check if a row exists.

        Example:
            Example calls are assuming an instance for table `user` for the
            central server.

            Check if usernames in combincation with address or not in
            combincation with address exists:
            >>> user.exists(username='testuser1', address='100 Davin Road')
            True
            >>> user.exists(username='testuser1')
            True
            >>> user.exists(username='testuser1', address='Wrong Address')
            False
            >>> user.exists(username='non existing username')
            False

        Args:
            kwargs: The keys (str) and values (str, int) for which it needs to
            be checked if a row exists.

        Returnes:
            bool: Whether a row exists or not.
        """
        with cursor() as cur:
            return len(self.export(self._primary_key, limit=1, **kwargs)) != 0


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
                ' WHERE ' + where(kwargs),
                tuple(kwargs.values())
            )


def init_mysql(app):
    # globally set mysql variable
    globals()['mysql'] = MySQL(app)
    if get_server_type() == ServerType.CENTRAL:
        sql_file = CENTRAL_SQL
    elif get_server_type() == ServerType.DATA:
        sql_file = DATA_SQL
    with cursor() as cur:
        with open(sql_file, 'r') as f:
            for q in f.read().split(';'):
                q = q.strip()
                if len(q) == 0:
                    continue
                q += ';'
                table = re.search(r'^[^\(]+?([a-zA-Z0-9]+)\s*\(', q).group(1)
                primary_key = re.search(r'([a-zA-Z0-9]+)\s+[^\s]+\s*PRIMARY\s*KEY', q).group(1)
                print('Creating table {} with primary key {}.'
                      .format(table, primary_key), flush=True)
                cur.execute(q)
                globals()[table] = TableLoader(table, primary_key)


def test_db():
    with cursor() as cur:
        cur.execute("INSERT INTO test VALUES (1)")
