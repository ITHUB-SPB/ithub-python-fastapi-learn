from datetime import datetime, UTC, timedelta

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from model import User

def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "iat": datetime.now(tz=UTC),
        "exp": datetime.now(tz=UTC) + timedelta(minutes=15),
    }

    return jwt.encode(
        payload=payload,
        key='yuacsyA97dcaunauibg3478zxc769xzc69sad',
        algorithm='HS256'
    )

def decode_token(access_token: str) -> dict[str, str]:
    payload = jwt.decode(
        access_token,
        key='yuacsyA97dcaunauibg3478zxc769xzc69sad',
        algorithms=['HS256']
    )

    return payload


def verify_password(
    session: Session,
    username: str,
    password_for_check: str
) -> bool:
    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalar_one()

    return user.password == password_for_check