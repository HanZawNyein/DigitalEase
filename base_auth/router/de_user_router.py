from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from base_database.middleware import get_db
from base_database.router import CRUDRouter
from base_database.services import CreateSchemaType
from ..constants import ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
from ..models.de_user_model import DeUserModel
from ..schema.de_token_schema import Token
from ..schema.de_user_schema import User
from ..services.token import authenticate_user, create_access_token, get_current_active_user


class DeUserRouter(CRUDRouter):
    model = DeUserModel
    create_schema = User
    update_schema = User
    response_model = User

    def init_routes(self):
        self.router.add_api_route("/token", self.login_for_access_token, methods=["POST"])
        self.router.add_api_route("/me", self.read_users_me, methods=["GET"], response_model=self.response_model)

    async def login_for_access_token(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> Token:
        user = authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "scopes": form_data.scopes},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")

    async def read_users_me(self,
            current_user: Annotated[User, Depends(get_current_active_user)],
    ):
        return current_user

    # async def login(self, obj_in, db: Session = Depends(get_db)):
    #     ...
    #
    # async def register(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
    #     ...
    #
    # async def forgot_password(self, obj_in, db: Session = Depends(get_db)):
    #     ...
    #
    # async def reset_password(self, obj_in, db: Session = Depends(get_db)):
    #     ...

    # Example of overriding a method
    # async def create_object(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
    #     obj_in.password = self.hash_password(obj_in.password)  # Example of custom logic
    #     return await super(DeUserRouter, self).create_object(obj_in, db)
    #
    # def hash_password(self, password: str) -> str:
    #     # Implement password hashing here
    #     return password + "hashed"


de_user_router = DeUserRouter().router
