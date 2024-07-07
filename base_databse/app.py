from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_object():
    return {"message": "Hello DB"}


@app.post("/")
async def post():
    return {"message": "Hello Create"}


@app.put("/")
async def put():
    return {"message": "Hello put"}


@app.delete("/")
async def delete():
    return {"message": "Hello delete"}
