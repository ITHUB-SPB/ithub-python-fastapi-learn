import typing

from fastapi import HTTPException, Depends, APIRouter

from database import Session, get_db_sqla
from database.users import insert_user
from schema import UserNew, UserPublic


users_api = APIRouter(
    prefix="/users",
    tags=['Пользователи и аккаунты']
)

@users_api.post('/', response_model=UserPublic, summary='Новый пользователь')
def post_user(
    payload: UserNew,
    session: typing.Annotated[Session, Depends(get_db_sqla)]
):
    try:
        return insert_user(new_user=payload, session=session)
    except Exception:
        raise HTTPException(status_code=400, detail="Ошибка при создании пользователя")
