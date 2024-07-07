from fastapi import FastAPI

from base import router
from base_databse.app import app as db_app

# from servers import servers

app = FastAPI(debug=True)
app.include_router(router)

# sub apps
app.mount('/auth', db_app)