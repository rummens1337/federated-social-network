from flaskext.mysql import MySQL


def init_mysql(app):
    # globally set mysql variable
    globals()['mysql'] = MySQL(app)


def db_test():
    # Test
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("INSERT INTO test VALUES (1)")
    con.commit()
    con.close()

