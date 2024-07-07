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

    # Example of overriding a method
    async def create_object(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
        obj_in.password = self.hash_password(obj_in.password)  # Example of custom logic
        return await super().create_object(obj_in, db)

    def hash_password(self, password: str) -> str:
        # Implement password hashing here
        return password + "hashed"


de_user_router = DeUserRouter().router
