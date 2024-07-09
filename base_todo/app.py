from fastapi import FastAPI, Depends

from base_auth.services.token import get_current_active_user
from base_todo.router.de_todo_router import DeTodoRouter

app = FastAPI(dependencies=[Depends(get_current_active_user)], title="Todo",)

app.include_router(DeTodoRouter().router)
