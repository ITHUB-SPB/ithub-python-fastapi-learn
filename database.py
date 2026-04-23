import sqlite3
import typing
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from connection import get_db, get_db_sa
from schema import Record, RecordCreate, UserCreate, UserResponse
from model import User

def select_records(
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
    search: str | None = None,
) -> list[Record]:
    where_statement = f'where user like "%{search}%"' if search else ''

    record_rows = cursor.execute(f'select * from records {where_statement}').fetchall()

    return [
        Record(id=record_row[0], course=record_row[1], user=record_row[2])
        for record_row in record_rows
    ]


def select_record_by_id(
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
    record_id: int
) -> Record | None:
    statement = 'select * from records where id = ?'
    record_row = cursor.execute(statement, (record_id,)).fetchone()

    if not record_row:
        return None

    return Record(id=record_row[0], course=record_row[1], user=record_row[2])


def insert_record(
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
    payload: RecordCreate
) -> Record:
    cursor.execute('''
        insert into records (course, user) values (?, ?)
    ''', (payload.course, payload.user))

    record_row = cursor.execute('''
        select * from records where id = ?
    ''', (cursor.lastrowid,)).fetchone()

    return Record(id=record_row[0], course=record_row[1], user=record_row[2])


def insert_user(
    session: typing.Annotated[Session, Depends(get_db_sa)],
    payload: UserCreate
):
    new_user = User(username=payload.username, password=payload.password)

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserResponse(id=new_user.id, username=new_user.username)
    except (IntegrityError, OperationalError) as exc:
        session.rollback()
        raise exc
