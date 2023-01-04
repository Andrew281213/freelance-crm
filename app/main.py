from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from .db import db
from .api import router as api_router
from .web import router as web_router

app = FastAPI(debug=False)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix="/api")
app.include_router(web_router)


class Settings(BaseModel):
	authjwt_secret_key: str = "super-puper secret key"
	authjwt_token_location: set = {"cookies"}
	authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
	return Settings()


@app.on_event("startup")
async def startup():
	await db.connect()


@app.on_event("shutdown")
async def shutdown():
	await db.disconnect()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
	response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
	response.delete_cookie("access_token")
	response.delete_cookie("access_token_cookie")
	return response
