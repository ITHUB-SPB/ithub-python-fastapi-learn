from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Record(BaseModel):
    id: int
    course: str
    user: str


class RecordCreate(BaseModel):
    course: str
    user: str


records = [
    { "id": 1, "course": "ОАиП", "user": "test" },
    { "id": 2, "course": "ОАиП", "user": "test-2" }
]

app = FastAPI(debug=True, title="Курсы", description="API")

@app.get('/records', response_model=list[Record], summary='Все записи')
def get_records(search: str | None = None) -> list[Record]:
    if not search:
        return [Record(**item) for item in records]

    return [Record(**item) for item in records if search in item['user']]


@app.get('/records/{record_id}', response_model=Record, summary='Запись по ID')
def get_record(record_id: int) -> Record:
    try:
        record_row = next(item for item in records if item["id"] == record_id)
        return Record(**record_row)
    except StopIteration:
        raise HTTPException(404, detail=f'Запись с id={record_id} не найдена')


@app.post('/records', response_model=Record, summary='Создание записи', status_code=201)
def post_record(payload: RecordCreate) -> Record:
    new_record = payload.model_dump()
    new_record['id'] = records[-1]['id'] + 1 if records else 1
    records.append(new_record)
    return Record(**records[-1])
