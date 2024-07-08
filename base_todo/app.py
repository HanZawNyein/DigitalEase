from fastapi import FastAPI, Depends

from base_auth.services.token import get_current_active_user
from base_todo.router.de_todo_router import DeTodoRouter

app = FastAPI()

app.include_router(DeTodoRouter().router, dependencies=[Depends(get_current_active_user)])
