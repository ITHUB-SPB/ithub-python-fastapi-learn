import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.sqlite', echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_db_sa():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


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
