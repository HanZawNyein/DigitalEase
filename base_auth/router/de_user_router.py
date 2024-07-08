from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from base_database.middleware import get_db
from base_database.router import CRUDRouter
from base_database.services import CreateSchemaType
from ..models.de_user_model import DeUserModel
from ..schema.de_user_schema import DeUserCreate, DeUserUpdate, DeUser


class DeUserRouter(CRUDRouter):
    model = DeUserModel
    create_schema = DeUserCreate
    update_schema = DeUserUpdate
    response_model = DeUser

    def init_routes(self):
        self.router.add_api_route("/register", self.register, response_model=self.response_model, methods=["POST"])
        self.router.add_api_route("/login", self.read_objects, response_model=List[self.response_model],
                                  methods=["POST"])
        self.router.add_api_route("/forgot-password", self.forgot_password, response_model=self.response_model,
                                  methods=["POST"])
        self.router.add_api_route("/reset-password", self.reset_password, response_model=self.response_model,
                                  methods=["POST"])

    async def login(self, obj_in, db: Session = Depends(get_db)):
        ...

    async def register(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
        ...

    async def forgot_password(self, obj_in, db: Session = Depends(get_db)):
        ...

    async def reset_password(self, obj_in, db: Session = Depends(get_db)):
        ...

    # Example of overriding a method
    # async def create_object(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
    #     obj_in.password = self.hash_password(obj_in.password)  # Example of custom logic
    #     return await super(DeUserRouter, self).create_object(obj_in, db)
    #
    # def hash_password(self, password: str) -> str:
    #     # Implement password hashing here
    #     return password + "hashed"


de_user_router = DeUserRouter().router
