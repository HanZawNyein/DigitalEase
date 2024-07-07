from typing import Type, Generic, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .middleware import get_db
from .services import CRUDGeneric, ModelType, CreateSchemaType, UpdateSchemaType


class CRUDRouter(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]
    create_schema: Type[CreateSchemaType]
    update_schema: Type[UpdateSchemaType]
    response_model: Type[BaseModel]

    def __init__(self):
        self.crud = CRUDGeneric[ModelType, CreateSchemaType, UpdateSchemaType](self.model)
        self.router = APIRouter()
        self.init_routes()

    def init_routes(self):
        self.router.add_api_route("/", self.read_objects, response_model=List[self.response_model], methods=["GET"])
        self.router.add_api_route("/", self.create_object, response_model=self.response_model, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_object, response_model=self.response_model, methods=["PUT"])
        self.router.add_api_route("/{id}", self.delete_object, response_model=self.response_model, methods=["DELETE"])

    async def read_objects(self, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return self.crud.get_multi(db=db, skip=skip, limit=limit)

    async def create_object(self, obj_in: CreateSchemaType, db: Session = Depends(get_db)):
        return self.crud.create(db=db, obj_in=obj_in)

    async def update_object(self, id: int, obj_in: UpdateSchemaType, db: Session = Depends(get_db)):
        db_obj = self.crud.get(db=db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return self.crud.update(db=db, db_obj=db_obj, obj_in=obj_in)

    async def delete_object(self, id: int, db: Session = Depends(get_db)):
        db_obj = self.crud.get(db=db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return self.crud.delete(db=db, id=id)
