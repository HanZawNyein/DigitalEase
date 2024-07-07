from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Type, Generic, List

from . import BaseModel
from .services import CRUDGeneric, ModelType, CreateSchemaType, UpdateSchemaType
from .middleware import get_db

class CRUDRouter(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], create_schema: Type[CreateSchemaType], update_schema: Type[UpdateSchemaType], response_model: Type[BaseModel]):
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_model = response_model
        self.crud = CRUDGeneric[ModelType, CreateSchemaType, UpdateSchemaType](model)
        self.router = APIRouter()

        @self.router.get("/", response_model=List[response_model])
        async def read_objects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            return self.crud.get_multi(db=db, skip=skip, limit=limit)

        @self.router.post("/", response_model=response_model)
        async def create_object(obj_in: create_schema, db: Session = Depends(get_db)):
            return self.crud.create(db=db, obj_in=obj_in)

        @self.router.put("/{id}", response_model=response_model)
        async def update_object(id: int, obj_in: update_schema, db: Session = Depends(get_db)):
            db_obj = self.crud.get(db=db, id=id)
            if not db_obj:
                raise HTTPException(status_code=404, detail="Object not found")
            return self.crud.update(db=db, db_obj=db_obj, obj_in=obj_in)

        @self.router.delete("/{id}", response_model=response_model)
        async def delete_object(id: int, db: Session = Depends(get_db)):
            db_obj = self.crud.get(db=db, id=id)
            if not db_obj:
                raise HTTPException(status_code=404, detail="Object not found")
            return self.crud.delete(db=db, id=id)
