from pydantic import BaseModel


class Record(BaseModel):
    id: int
    course: str
    user: str


class RecordCreate(BaseModel):
    course: str
    user: str


class User(BaseModel):
    id: int
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str