from sqlalchemy import VARCHAR, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.exc import IntegrityError, OperationalError

from schema import UserNew, UserPublic
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(15), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


def insert_user(
    new_user: UserNew,
    session: Session
) -> User:
    created_user = User(username=new_user.username, password=new_user.password)

    try:
        session.add(created_user)
        session.commit()
        session.refresh(created_user)
        return created_user
    except (IntegrityError, OperationalError) as exc:
        session.rollback()
        raise exc


def select_user_by_username(
    session: Session,
    username: str
) -> UserPublic | None:
    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalar_one_or_none()

    if not user:
        return None

    return UserPublic(id=user.id, username=user.username)