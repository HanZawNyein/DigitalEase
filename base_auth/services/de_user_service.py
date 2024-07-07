from sqlalchemy.orm import Session

from ..models.de_user_model import DeUserModel
from ..schema.de_user_schema import DeUserCreate


def get_user(db: Session, user_id: int):
    return db.query(DeUserModel).filter(DeUserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(DeUserModel).filter(DeUserModel.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeUserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: DeUserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = DeUserModel(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
