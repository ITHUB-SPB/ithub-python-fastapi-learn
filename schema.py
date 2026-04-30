from pydantic import BaseModel, Field


class Record(BaseModel):
    id: int
    course_id: int
    payment_id: int
    user: str


class RecordNew(BaseModel):
    course_id: int
    payment_id: int
    user: str


class User(BaseModel):
    id: int
    username: str
    password: str


class UserNew(BaseModel):
    username: str
    password: str = Field(min_length=6)


class UserPublic(BaseModel):
    id: int
    username: str
