from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT

from app.api.v1.users.routes import login as api_login
from app.api.v1.users.schemas import UserCreate

from .forms import LoginForm

templates = Jinja2Templates("app/templates")
router = APIRouter(include_in_schema=False)


@router.get("/login")
async def login(request: Request):
	if request.cookies.get("access_token_cookie") is not None:
		return RedirectResponse("/", status_code=302)
	return templates.TemplateResponse("users/login.html", {"request": request})


@router.post("/login")
async def login(request: Request, jwt: AuthJWT = Depends()):
	form = LoginForm(request)
	await form.load_data()
	if form.is_valid():
		user = UserCreate(username=form.username, password=form.password)
		response = await api_login(user, jwt=jwt)
		if response is not None and response.get("username") is not None:
			return RedirectResponse("/", status_code=302)
