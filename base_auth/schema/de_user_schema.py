from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class RegisterUser(BaseUser):
    password: str
    confirm_password: str


class User(BaseUser):
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
