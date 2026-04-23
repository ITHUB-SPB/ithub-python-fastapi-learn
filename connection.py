import sqlite3

def get_db():
    connection = sqlite3.connect('database.sqlite', check_same_thread=False)
    try:
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        connection.rollback()
    finally:
        connection.close()
