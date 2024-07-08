from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from base_auth.models.de_user_model import DeUserModel
from base_auth.schema.de_user_schema import User
from base_database.middleware import get_db
from base_database.router import CRUDRouter
from base_database.services import CreateSchemaType

class DeTodoRouter(CRUDRouter):
    model = DeUserModel
    # create_schema = User
    # update_schema = User
    # response_model = User

    def init_routes(self):
        self.router.add_api_route("/home", self.get_todos, methods=["GET"])

    def get_todos(self):
        ...

de_user_router = DeTodoRouter().router
