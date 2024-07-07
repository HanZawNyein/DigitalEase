from typing import Type, List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import Column, inspect
from sqlalchemy.orm import Session

from .database import BaseModel, SessionLocal


# Function to dynamically create SQLAlchemy models
def create_dynamic_model(table_name: str, columns: dict):
    attrs = {'__tablename__': table_name}

    # Iterate over columns dictionary to define each column
    for col_name, col_type in columns.items():
        # Ensure 'id' column is marked as primary key
        if col_name == 'id':
            attrs[col_name] = Column(col_type, primary_key=True)
        else:
            attrs[col_name] = Column(col_type)

    # Create the dynamic model class
    DynamicModel = type(table_name.capitalize(), (BaseModel,), attrs)

    return DynamicModel


# Function to generate Pydantic schemas
def generate_pydantic_schema(model: Type[BaseModel]):
    schema_attrs = {}
    mapper = inspect(model)
    for column in mapper.columns:
        schema_attrs[column.key] = (column.type.python_type, ...)
        # Handle specific types or constraints as needed

    schema_name = f'{model.__name__}Schema'
    schema = type(schema_name, (BaseModel,), schema_attrs)
    return schema

# Function to create dynamic CRUD router
def create_dynamic_router(model: Type[BaseModel]):
    schema = generate_pydantic_schema(model)
    router = APIRouter()

    @router.get("/", response_model=List[schema])
    def read_objects(skip: int = 0, limit: int = 100, db: Session = Depends(SessionLocal)):
        return db.query(model).offset(skip).limit(limit).all()

    @router.post("/", response_model=schema)
    def create_object(item: schema, db: Session = Depends(SessionLocal)):
        db_item = model(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.put("/{item_id}", response_model=schema)
    def update_object(item_id: int, item: schema, db: Session = Depends(SessionLocal)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        for field, value in item.dict().items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.delete("/{item_id}", response_model=schema)
    def delete_object(item_id: int, db: Session = Depends(SessionLocal)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return db_item

    return router