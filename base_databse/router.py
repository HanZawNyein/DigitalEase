from fastapi import APIRouter

crud_router = APIRouter()


@crud_router.get("/")
async def read_objects():
    return {"message": "Hello DB"}


@crud_router.post("/")
async def create_objects():
    return {"message": "Hello Create"}


@crud_router.put("/")
async def update_objects():
    return {"message": "Hello put"}


@crud_router.delete("/")
async def delete_objects():
    return {"message": "Hello delete"}
