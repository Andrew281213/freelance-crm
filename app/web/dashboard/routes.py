from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT


templates = Jinja2Templates("app/templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
def main(request: Request, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	username = jwt.get_jwt_subject()
	return templates.TemplateResponse("dashboard/main.html", {"request": request, "user": {"username": username}})


@router.get("/orders")
def orders(request: Request, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	username = jwt.get_jwt_subject()
	return templates.TemplateResponse("dashboard/orders.html", {"request": request, "user": {"username": username}})


@router.get("/clients")
def clients(request: Request, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	username = jwt.get_jwt_subject()
	return templates.TemplateResponse("dashboard/clients.html", {"request": request, "user": {"username": username}})


@router.get("/parsers")
def parsers(request: Request, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	username = jwt.get_jwt_subject()
	return templates.TemplateResponse("dashboard/parsers.html", {"request": request, "user": {"username": username}})
