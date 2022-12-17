from fastapi import FastAPI
from .db import db
from app.api.v1.users.routes import router as users_router

app = FastAPI(debug=False)


@app.on_event("startup")
async def startup():
	await db.connect()


@app.on_event("shutdown")
async def shutdown():
	await db.disconnect()


app.include_router(users_router, prefix="/users")


@app.get("/")
def hello():
	return {"hello": "world"}
