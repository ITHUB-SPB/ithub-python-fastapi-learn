import sqlite3
from fastapi import FastAPI

from connection import engine
from model import Base

from api.api_records import records_router
from api.api_users import users_router

app = FastAPI(debug=True, title="Курсы", description="API")

app.include_router(records_router)
app.include_router(users_router)

@app.on_event("startup")
def startup_event():
    connection = sqlite3.connect('database.sqlite', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute('''
        create table if not exists records (
        id integer primary key,
        course varchar(50) not null,
        user varchar(20) not null
    )''')
    connection.commit()
    connection.close()

    Base.metadata.create_all(bind=engine)

