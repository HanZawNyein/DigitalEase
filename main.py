from fastapi import FastAPI, Request, Response

from base import router
from base_auth.app import app as base_auth
# sub apps
from base_database.app import app as base_database
from base_database.database import BaseModel, engine, SessionLocal

BaseModel.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except Exception as e:
        raise e
    finally:
        request.state.db.close()
    return response


app.include_router(router)

# sub apps
app.mount('/database', base_database)
app.mount('/auth', base_auth)
