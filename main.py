from fastapi import FastAPI

from base import router
from base_databse import app as db_app
from servers import servers

app = FastAPI(debug=True, servers=servers)
app.include_router(router)

# sub apps
app.mount('/database', db_app)
