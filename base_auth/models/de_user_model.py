from sqlalchemy import Boolean, Column, Integer, String

from base_databse.database import BaseModel


class DeUserModel(BaseModel):
    __tablename__ = "de_user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)