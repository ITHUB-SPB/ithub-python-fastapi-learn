import sqlite3
import typing
from fastapi import Depends
from connection import get_db
from schema import Record, RecordCreate

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
):
    cursor.execute('''
        insert into records (course, user) values (?, ?)
    ''', (payload.course, payload.user))

    record_row = cursor.execute('''
        select * from records where id = ?
    ''', (cursor.lastrowid,)).fetchone()

    return Record(id=record_row[0], course=record_row[1], user=record_row[2])
