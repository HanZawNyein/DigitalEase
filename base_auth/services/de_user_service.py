from sqlalchemy.orm import Session

from base_database.services import create_generic_crud
from ..models.de_user_model import DeUserModel
from ..schema.de_user_schema import DeUserCreate

DeUser = create_generic_crud(DeUserModel)


def get_user(db: Session, user_id: int):
    return DeUser.get(db, user_id=user_id)


def get_user_by_email(db: Session, email: str):
    return DeUser.get_by(db, email=email)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return DeUser.get_multi(db, skip=skip, limit=limit)


def create_user(db: Session, user: DeUserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = DeUserModel(email=user.email, hashed_password=fake_hashed_password)
    return DeUser.create(db, db_user)
