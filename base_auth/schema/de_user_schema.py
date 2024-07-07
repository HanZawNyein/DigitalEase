from pydantic import BaseModel


class DeUserBase(BaseModel):
    email: str


class DeUserCreate(DeUserBase):
    password: str


class DeUser(DeUserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
