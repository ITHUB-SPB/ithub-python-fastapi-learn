import sqlite3
import typing

from fastapi import HTTPException, Depends, APIRouter

from database import get_db
from database.records import select_records, select_record, insert_record
from schema import Record, RecordNew

records_api = APIRouter(
    prefix="/records",
    tags=['Заявки']
)

@records_api.get('/', response_model=list[Record], summary='Все заявки')
def get_records(
        cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)],
        search: str | None = None
):
    return select_records(cursor=cursor, search=search)


@records_api.get('/{record_id}', response_model=Record, summary='Заявка по ID')
def get_record(
        record_id: int,
        cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)]
):
    record = select_record(record_id=record_id, cursor=cursor)

    if not record:
        raise HTTPException(404, f'Заявка с id={record_id} не найдена')

    return record


@records_api.post('/', response_model=Record, summary='Новая заявка')
def post_record(
    payload: RecordNew,
    cursor: typing.Annotated[sqlite3.Cursor, Depends(get_db)]
):
    new_record_id = insert_record(new_record=payload, cursor=cursor)
    return select_record(record_id=new_record_id, cursor=cursor)
