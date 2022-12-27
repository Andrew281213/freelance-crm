from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from .forms import LoginForm

templates = Jinja2Templates("app/templates")
router = APIRouter(include_in_schema=False)


@router.get("/login")
async def login(request: Request):
	return templates.TemplateResponse("users/login.html", {"request": request})


@router.post("/login")
async def login(request: Request):
	form = LoginForm(request)
	await form.load_data()
	if form.is_valid():
		# TODO: Сделать проверку формы авторизации
		pass
