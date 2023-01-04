from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .schemas import ClientCreate, UrlCreate, NicknameCreate, UrlPublic, ClientPublic, NicknamePublic, NicknameUpdate
from .models import Client, ClientUrl, ClientNickname

from fastapi_jwt_auth import AuthJWT
from asyncpg.exceptions import UniqueViolationError

router = APIRouter(
	responses={
		404: {"description": "Страница не найдена"},
	}
)


@router.get(
	"/nicknames/{id}", response_model=NicknamePublic, status_code=200,
	description="Получить информацию о нике по id",
	responses={
		200: {
			"description": "Успешный запрос"
		}
	}
)
async def get_nickname(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	nickname = await ClientNickname.get(id)
	if nickname is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ник не найден")
	return NicknamePublic(**nickname.dict()).dict()


@router.post("/nicknames", status_code=status.HTTP_200_OK, description="Создать новый ник")
async def create_nickname(nickname: NicknameCreate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	try:
		nickname_id = await ClientNickname.create(nickname)
	except UniqueViolationError:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой ник уже зарегистрирован")
	return {"nickname_id": nickname_id}


@router.put("/nicknames/{id}", status_code=status.HTTP_202_ACCEPTED, description="Изменить ник")
async def change_nickname(id: int, nickname: NicknameUpdate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	nickname = await ClientNickname.update(id=id, nickname=nickname)
	if nickname is None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ник не найден")
	return NicknamePublic(**nickname.dict()).dict()


@router.delete("/nicknames/{id}", status_code=status.HTTP_200_OK, description="Удалить ник")
async def delete_nickname(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	nickname_id = await ClientNickname.delete(id)
	if nickname_id is None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ник не найден")
	return {"nickname_id": nickname_id}
