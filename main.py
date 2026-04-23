import sqlite3
import typing
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from schema import RecordCreate, Record, UserResponse, UserCreate
from database import select_records, select_record_by_id, insert_record, insert_user
from connection import get_db, get_db_sa, engine
from model import Base

app = FastAPI(debug=True, title="Курсы", description="API")

@app.on_event("startup")
def startup_event():
    connection = sqlite3.connect('database.sqlite', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        create table if not exists records (
        id integer primary key,
        course varchar(50) not null,
        user varchar(20) not null
    )''')
    connection.commit()
    connection.close()

    Base.metadata.create_all(bind=engine)


@app.get(
    '/records',
    response_model=list[Record],
    summary='Все записи'
)
def get_records(
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
    search: str | None = None,
) -> list[Record]:
    return select_records(cursor=cursor, search=search)


@app.get(
    '/records/{record_id}',
    response_model=Record,
    summary='Запись по ID',
    responses={ 404: { "description": "Запись не найдена" } }
)
def get_record(
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
    record_id: int
) -> Record:
    record = select_record_by_id(cursor=cursor, record_id=record_id)

    if not record:
        raise HTTPException(404, detail=f'Запись с id={record_id} не найдена')

    return record


@app.post(
    '/records',
    response_model=Record,
    summary='Создание записи',
    status_code=201
)
def post_record(
        cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
        payload: RecordCreate
) -> Record:
    return insert_record(cursor=cursor, payload=payload)


@app.post(
    '/users',
    response_model=UserResponse,
    summary='Создание аккаунта',
    status_code=201
)
def post_user(
    session: typing.Annotated[Session, Depends(get_db_sa)],
    payload: UserCreate
) -> UserResponse:
    try:
        return insert_user(session=session, payload=payload)
    except Exception:
        raise HTTPException(status_code=409, detail="Invalid payload")
