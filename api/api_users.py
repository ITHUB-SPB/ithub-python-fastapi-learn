import typing
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schema import UserResponse, UserCreate, UserToken
from database.service_users import insert_user, get_user_by_username
from database.service_auth import verify_password, create_access_token
from connection import get_db_sa

users_router = APIRouter()

@users_router.post(
    '/users',
    response_model=UserResponse,
    summary='Создание аккаунта',
    status_code=201,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Юзернейм уже зарегистрирован"}
    }
)
def post_user(
    session: typing.Annotated[Session, Depends(get_db_sa)],
    payload: UserCreate
) -> UserResponse:
    try:
        return insert_user(session=session, payload=payload)
    except Exception:
        raise HTTPException(status_code=409, detail="Юзернейм уже зарегистрирован")


@users_router.post(
    '/users/login',
    response_model=UserToken,
    summary='Логин',
    responses={
        status.HTTP_401_UNAUTHORIZED: { "description": "Неверный логин или пароль" }
    }
)
def login_user(
    session: typing.Annotated[Session, Depends(get_db_sa)],
    credentials: typing.Annotated[OAuth2PasswordRequestForm, Depends()]
) -> UserToken:
    user = get_user_by_username(session=session, username=credentials.username)

    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    if not verify_password(session=session, username=user.username, password_for_check=credentials.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    access_token = create_access_token(username=user.username)

    return UserToken(access_token=access_token)