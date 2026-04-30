from fastapi import FastAPI
from database import Base, engine
from api.records import records_api
from api.users import users_api

app = FastAPI(
    title='Заявки',
    description='API',
    debug=True
)

app.include_router(records_api)
app.include_router(users_api)


@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)




