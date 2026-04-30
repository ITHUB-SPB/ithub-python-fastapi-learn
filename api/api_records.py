import sqlite3
import typing

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from schema import RecordCreate, Record
from database.service_records import select_records, select_record_by_id, insert_record
from database.service_auth import decode_token
from database.service_users import get_user_by_username
from connection import get_db

oauth2 = OAuth2PasswordBearer('/users/login')

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
    payload: RecordCreate,
    token: typing.Annotated[oauth2, Depends()]
) -> Record:
    username = decode_token(token).get('username')

    if not username:
        raise HTTPException(status_code=401, detail="Отсутствуют пользовательские данные")

    if not get_user_by_username(username):
        raise HTTPException(status_code=401, detail="Отсутствуют пользовательские данные")

    return insert_record(cursor=cursor, payload=payload)
