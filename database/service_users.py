import typing
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from connection import get_db_sa
from schema import UserCreate, UserResponse
from model import User


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
