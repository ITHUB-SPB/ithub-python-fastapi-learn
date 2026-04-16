import sqlite3
import typing
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel


def get_db():
    connection = sqlite3.connect('database.sqlite', check_same_thread=False)
    try:
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
    finally:
        connection.close()


# def create_table_records():
#     connection = get_db()
#     cursor = connection.cursor()
#     cursor.execute('''
#         create table if not exists records (
#         id integer primary key,
#         course varchar(50) not null,
#         user varchar(20) not null
#     )''')
#     connection.commit()
#     connection.close()


class Record(BaseModel):
    id: int
    course: str
    user: str


class RecordCreate(BaseModel):
    course: str
    user: str


app = FastAPI(debug=True, title="Курсы", description="API")

# @app.on_event("startup")
# def startup_event():
#     create_table_records()


@app.get('/records', response_model=list[Record], summary='Все записи')
def get_records(
        cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
        search: str | None = None,
) -> list[Record]:
    where_statement = f'where user like "%{search}%"' if search else ''

    record_rows = cursor.execute(f'select * from records {where_statement}').fetchall()

    return [
        Record(id=record_row[0], course=record_row[1], user=record_row[2])
        for record_row in record_rows
    ]


@app.get('/records/{record_id}', response_model=Record, summary='Запись по ID')
def get_record(record_id: int) -> Record:
    connection = get_db()
    cursor = connection.cursor()

    statement = 'select * from records where id = ?'
    record_row = cursor.execute(statement, (record_id,)).fetchone()
    connection.close()

    if not record_row:
        raise HTTPException(404, detail=f'Запись с id={record_id} не найдена')

    return Record(id=record_row[0], course=record_row[1], user=record_row[2])


@app.post('/records', response_model=Record, summary='Создание записи', status_code=201)
def post_record(payload: RecordCreate) -> Record:
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute('''
        insert into records (course, user) values (?, ?)
    ''', (payload.course, payload.user))

    connection.commit()

    record_row = cursor.execute('''
        select * from records where id = ?
    ''', (cursor.lastrowid,)).fetchone()

    connection.close()
    return Record(id=record_row[0], course=record_row[1], user=record_row[2])
