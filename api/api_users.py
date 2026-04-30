import typing
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from schema import UserResponse, UserCreate
from database.service_users import insert_user
from connection import get_db_sa

users_router = APIRouter()

@users_router.post(
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
