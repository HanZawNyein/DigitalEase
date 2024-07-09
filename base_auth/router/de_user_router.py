from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from base_database.middleware import get_db
from base_database.router import CRUDRouter
from ..constants import ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
from ..models.de_user_model import DeUserModel
from ..schema.de_token_schema import Token
from ..schema.de_user_schema import User, RegisterUser, BaseUser, UserInDB
from ..services.token import authenticate_user, create_access_token, get_current_active_user


class DeUserRouter(CRUDRouter):
    model = DeUserModel
    create_schema = User
    update_schema = User
    response_model = User

    def init_routes(self):
        self.router.add_api_route("/token", self.login_for_access_token, methods=["POST"])
        self.router.add_api_route("/me", self.read_users_me, methods=["GET"], response_model=self.response_model)
        self.router.add_api_route("/register", self.register, methods=["POST"], response_model=BaseUser)

    async def register(self, register_user: RegisterUser, db: Session = Depends(get_db)) -> BaseUser:
        newUser = {
            "username": register_user.username,
            "email": register_user.email,
            "full_name": register_user.full_name,
            "hashed_password": register_user.password,
            "disabled": False,
        }
        new_user = UserInDB(**newUser)
        result = await self.create_object(new_user, db=db)
        return BaseUser(**new_user.dict())

    # async def create_object(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
    #         return self.crud.create(db=db, obj_in=obj_in)

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


de_user_router = DeUserRouter().router
