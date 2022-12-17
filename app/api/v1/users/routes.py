from fastapi import APIRouter, HTTPException, Query
from .schemas import UserPublic, UserCreate
from .models import User
from app.utils.hasher import Hasher
from asyncpg.exceptions import UniqueViolationError

router = APIRouter(
	tags=["users"],
	responses={
		404: {"description": "Страница не найдена"}
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
	return UserPublic(**user).dict()


@router.post(
	"", status_code=200, description="Создать нового пользователя",
)
async def create_user(user: UserCreate):
	user.password = Hasher.hash_password(user.password)
	try:
		user_id = await User.create(user)
	except UniqueViolationError:
		raise HTTPException(status_code=409, detail="Пользователь с таким ником уже зарегистрирован")
	return {"user_id": user_id}
