from base_auth.schema.de_user_schema import DeUser, DeUserCreate, DeUserBase, DeUserUpdate
from base_database.router import CRUDRouter
from ..models.de_user_model import DeUserModel

# router = APIRouter()
# router = CRUDRouter(DeUserModel, DeUserCreate,DeUser).router
de_user_router = CRUDRouter(DeUserModel, DeUserCreate, DeUserUpdate,DeUser).router
# de_user_router = CRUDRouter(DeUserModel, DeUserCreate, DeUserUpdate, DeUser)

# class DeUserRouter(CRUDRouter):
#     model = DeUserModel
#     create_schema = DeUserCreate
#     update_schema = DeUserUpdate
#     response_model = DeUser
#
# de_user_router = DeUserRouter()

#
#
# @router.post("/users/", response_model=DeUser)
# def create_user(user: DeUserCreate, db: Session = Depends(get_db)):
#     db_user = de_user_service.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return de_user_service.create_user(db=db, user=user)
#
# @router.get("/users/", response_model=list[DeUser])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = de_user_service.get_users(db, skip=skip, limit=limit)
#     return users
