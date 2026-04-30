import typing

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from database import Session, get_db_sqla
from database.users import insert_user
from schema import UserNew, UserPublic


users_api = APIRouter(
    prefix="/users",
    tags=['Пользователи и аккаунты']
)

@users_api.post('/', response_model=UserPublic, summary='Новый пользователь')
def register(
    payload: UserNew,
    session: typing.Annotated[Session, Depends(get_db_sqla)]
):
    try:
        return insert_user(new_user=payload, session=session)
    except Exception:
        raise HTTPException(status_code=400, detail="Ошибка при создании пользователя")


@users_api.post(
    '/login',
    response_model=UserPublic,
    summary='Логин'
)
def login(
    payload: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    session: typing.Annotated[Session, Depends(get_db_sqla)]
):
    try:
        return insert_user(new_user=payload, session=session)
    except Exception:
        raise HTTPException(status_code=400, detail="Ошибка при создании пользователя")
