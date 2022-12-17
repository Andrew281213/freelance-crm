from fastapi import FastAPI
from .db import db
from .models import User as UserModel
from .schema import User as UserSchema

app = FastAPI(debug=True)


@app.on_event("startup")
async def startup():
	await db.connect()


@app.on_event("shutdown")
async def shutdown():
	await db.disconnect()


@app.get("/")
def hello():
	return {"hello": "world"}


@app.post("/users/")
async def create_user(user: UserSchema):
	user_id = await UserModel.create(**user.dict())
	return {"user_id": user_id}


@app.get("/users/{id}", response_model=UserSchema)
async def get_user(id: int):
	user = await UserModel.get(idx=id)
	return UserSchema(**user).dict()
