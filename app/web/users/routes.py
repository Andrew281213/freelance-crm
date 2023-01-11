from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from starlette import status

from app.api.v1.users.routes import login as api_login
from app.api.v1.users.schemas import UserCreate

from .forms import LoginForm

templates = Jinja2Templates("app/templates")
router = APIRouter(include_in_schema=False)


@router.get("/login")
async def get_login(request: Request):
	if request.cookies.get("access_token_cookie") is not None:
		return RedirectResponse("/", status_code=302)
	return templates.TemplateResponse("users/login.html", {"request": request})


@router.post("/login")
async def post_login(request: Request, jwt: AuthJWT = Depends()):
	form = LoginForm(request)
	await form.load_data()
	if form.is_valid():
		user = UserCreate(username=form.username, password=form.password)
		try:
			response = await api_login(user, jwt=jwt)
		except HTTPException as e:
			errors = [e.detail]
			return templates.TemplateResponse("users/login.html", {"request": request, "errors": errors})
		if response is not None and response.get("username") is not None:
			return RedirectResponse("/", status_code=302, headers=jwt._response.headers)


@router.get("/logout")
async def logout(request: Request, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
	jwt.unset_jwt_cookies(response)
	return response
