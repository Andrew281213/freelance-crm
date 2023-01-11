from datetime import timedelta

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from app.utils.hasher import Hasher
from .models import User
from .schemas import UserPublic, UserCreate

router = APIRouter(
	responses={
		404: {"description": "Страница не найдена"},
	}
)


@router.get(
	"/{id}", response_model=UserPublic, status_code=200,
	description="Получить информацию о пользователе по id",
	responses={
		200: {
			"description": "Успешный запрос",
			"content": {
				"application/json": {
					"example": {
						"id": 1, "username": "Admin"
					}
				}
			}
		}
	}
)
async def get_user(id: int):
	user = await User.get(id=id)
	if user is None:
		raise HTTPException(status_code=404, detail="Пользователь не найден")
	return user.dict()


@router.post(
	"/", status_code=200, description="Создать нового пользователя",
)
async def create_user(user: UserCreate):
	user.password = Hasher.hash_password(user.password)
	try:
		user_id = await User.create(user)
	except UniqueViolationError:
		raise HTTPException(status_code=409, detail="Пользователь с таким ником уже зарегистрирован")
	return {"user_id": user_id}


@router.post(
	"/login", response_model=UserPublic, status_code=200, description="Авторизовать пользователя"
)
async def login(user: UserCreate, jwt: AuthJWT = Depends()):
	db_user = await User.get_by_username(username=user.username)
	if db_user is None:
		raise HTTPException(status_code=401, detail="Неверно введен логин или пароль")
	if not Hasher.verify_password(password=user.password, hashed_password=db_user.password):
		raise HTTPException(status_code=401, detail="Неверно введен логин или пароль")
	access_token = jwt.create_access_token(subject=user.username, expires_time=timedelta(hours=12))
	jwt.set_access_cookies(access_token)
	return UserPublic(**db_user.dict()).dict()


@router.delete("/logout")
async def logout(jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	jwt.unset_jwt_cookies()
	return {"detail": "Выход успешно выполнен"}


@router.get("/me/")
async def get_me(jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	username = jwt.get_jwt_subject()
	current_user = await User.get_by_username(username)
	return UserPublic(**current_user.dict())
