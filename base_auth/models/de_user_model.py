from sqlalchemy import Boolean, Column, Integer, String

from base_database.database import BaseModel


class DeUserModel(BaseModel):
    __tablename__ = "de_user2"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)