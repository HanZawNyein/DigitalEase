from typing import Optional

from pydantic import BaseModel


class DeUserBase(BaseModel):
    email: str


class DeUserCreate(DeUserBase):
    password: str
class DeUserUpdate(DeUserBase):
    password: Optional[str] = None

class DeUser(DeUserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
