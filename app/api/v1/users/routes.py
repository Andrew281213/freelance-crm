from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from .models import User
from .schemas import UserPublic, UserCreate, Token, UserInDB
from .utils import Hasher
from .utils import authenticate_user, create_access_token, get_current_user

base_responses = {
	status.HTTP_200_OK: {
		"description": "Успешный запрос"
	},
	status.HTTP_404_NOT_FOUND: {
		"description": "Пользователь не найден",
		"content": {
			"application/json": {
				"example": {"detail": "Пользователь с таким id не найден"}
			}
		}
	},
	status.HTTP_401_UNAUTHORIZED: {
		"description": "Ошибка авторизации",
		"content": {
			"application/json": {
				"example": {"detail": "Not authenticated"}
			}
		}
	},
	status.HTTP_422_UNPROCESSABLE_ENTITY: {
		"description": "Ошибка валидации данных",
		"content": {
			"application/json": {
				"example": {"detail": "Отсутствуют обязательные поля: password, username"}
			}
		}
	}
}

router = APIRouter()


@router.get(
	"/{id}", response_model=UserPublic, status_code=status.HTTP_200_OK,
	description="Получить информацию о пользователе по id",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_422_UNPROCESSABLE_ENTITY: base_responses[status.HTTP_422_UNPROCESSABLE_ENTITY],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_404_NOT_FOUND: base_responses[status.HTTP_404_NOT_FOUND],
	}
)
async def get_user(id: int):
	user = await User.get(id=id)
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с таким id не найден"
		)
	return user.dict()


@router.post(
	"/", status_code=status.HTTP_200_OK,
	description="Создание нового пользователя",
	responses={
		status.HTTP_200_OK: {
			"description": base_responses[status.HTTP_200_OK].get("description"),
			"content": {
				"application/json": {
					"example": {"user_id": 1}
				}
			}
		},
		status.HTTP_422_UNPROCESSABLE_ENTITY: base_responses[status.HTTP_422_UNPROCESSABLE_ENTITY],
		status.HTTP_409_CONFLICT: {
			"description": "Пользователь с таким ником уже зарегистрирован",
			"content": {
				"application/json": {
					"example": {"detail": "Пользователь с таким ником уже зарегистрирован"}
				}
			}
		},
	}
)
async def create_user(user: UserCreate):
	user.password = Hasher.hash_password(user.password)
	try:
		user_id = await User.create(user)
	except UniqueViolationError:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Пользователь с таким ником уже зарегистрирован"
		)
	return {"user_id": user_id}


@router.post(
	"/token", response_model=Token,
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_422_UNPROCESSABLE_ENTITY: base_responses[status.HTTP_422_UNPROCESSABLE_ENTITY],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
	}
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	user = await authenticate_user(
		username=form_data.username, password=form_data.password
	)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Неверно введен логин или пароль",
			headers={"WWW-Authenticate": "Bearer"}
		)
	access_token = create_access_token(data={"sub": form_data.username})
	return {"access_token": access_token, "token_type": "Bearer"}


@router.get(
	"/me/", status_code=status.HTTP_200_OK, response_model=UserPublic,
	description="Вывод информации о текущем авторизованном пользователе",
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_422_UNPROCESSABLE_ENTITY: base_responses[status.HTTP_422_UNPROCESSABLE_ENTITY],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_404_NOT_FOUND: base_responses[status.HTTP_404_NOT_FOUND],
	}
)
async def get_me(user: UserInDB = Depends(get_current_user)):
	return UserPublic(**user.dict())
