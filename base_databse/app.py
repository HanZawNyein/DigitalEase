from fastapi import FastAPI

from .router import crud_router

app = FastAPI()
app.include_router(crud_router)
