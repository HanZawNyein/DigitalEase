from fastapi import FastAPI

from .router.de_user_router import de_user_router

app = FastAPI(title='Auth')

app.include_router(de_user_router,tags=['User Authentication'])
