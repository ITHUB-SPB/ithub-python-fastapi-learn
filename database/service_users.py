import typing
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from connection import get_db_sa
from schema import UserCreate, UserResponse
from model import User


def get_user_by_username(
    session: typing.Annotated[Session, Depends(get_db_sa)],
    username: str
) -> UserResponse | None:
    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalar_one_or_none()

    if not user:
        return None

    return UserResponse(id=user.id, username=user.username)


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
