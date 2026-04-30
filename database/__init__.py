import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


def get_db_sqla():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_db():
    connection = sqlite3.connect('records.sqlite3')

    try:
        yield connection.cursor()
    except sqlite3.IntegrityError:
        connection.rollback()
    else:
        connection.commit()

    connection.close()


engine = create_engine('sqlite:///records.sqlite3', echo=True)
Session = sessionmaker(bind=engine, autoflush=False)