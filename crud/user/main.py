from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from app import router as UserRoute
from app import api as ApiRouter

app=FastAPI()
app.include_router(UserRoute.router)
app.include_router(ApiRouter.app,tags=["api"])

register_tortoise(
    app,
    db_url="postgres://postgres:root@127.0.0.1/crud",
    modules={'models':['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
