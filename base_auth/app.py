from fastapi import FastAPI

from .router.de_user_router import router

app = FastAPI(title='Auth')

app.include_router(router,tags=['Authentication'])
