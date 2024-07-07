from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from base_auth.schema.de_user_schema import DeUser, DeUserCreate
from base_database.middleware import get_db
from ..services import de_user_service

router = APIRouter()


@router.post("/users/", response_model=DeUser)
def create_user(user: DeUserCreate, db: Session = Depends(get_db)):
    db_user = de_user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return de_user_service.create_user(db=db, user=user)
