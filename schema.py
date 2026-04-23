from pydantic import BaseModel


class Record(BaseModel):
    id: int
    course: str
    user: str


class RecordCreate(BaseModel):
    course: str
    user: str
