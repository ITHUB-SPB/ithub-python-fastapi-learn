import sqlite3
import typing
from fastapi import HTTPException, Depends, APIRouter

from schema import RecordCreate, Record
from database.service_records import select_records, select_record_by_id, insert_record
from connection import get_db

records_router = APIRouter()

@records_router.get(
    '/records',
    response_model=list[Record],
    summary='Все записи'
)
def get_records(
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
    search: str | None = None,
) -> list[Record]:
    return select_records(cursor=cursor, search=search)


@records_router.get(
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


@records_router.post(
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
