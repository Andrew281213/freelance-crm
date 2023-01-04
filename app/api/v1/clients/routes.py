from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .schemas import ClientCreate, UrlCreate, NicknameCreate, UrlPublic, ClientPublic, NicknamePublic, NicknameUpdate, \
	UrlUpdate
from .models import Client, ClientUrl, ClientNickname

from fastapi_jwt_auth import AuthJWT
from asyncpg.exceptions import UniqueViolationError

base_responses = {
		404: {"description": "Страница не найдена"},
	}

nicknames_router = APIRouter(responses=base_responses, prefix="/nicknames")
urls_router = APIRouter(responses=base_responses, prefix="/urls")


@nicknames_router.get(
	"/nicknames/{id}", response_model=NicknamePublic, status_code=200,
	description="Получить информацию о нике по id",
	responses={
		200: {
			"description": "Успешный запрос"
		}
	},
)
async def get_nickname(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	nickname = await ClientNickname.get(id)
	if nickname is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ник не найден")
	return NicknamePublic(**nickname.dict()).dict()


@nicknames_router.post("/", status_code=status.HTTP_200_OK, description="Создать новый ник")
async def create_nickname(nickname: NicknameCreate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	try:
		nickname_id = await ClientNickname.create(nickname)
	except UniqueViolationError:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой ник уже зарегистрирован")
	return {"nickname_id": nickname_id}


@nicknames_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, description="Изменить ник")
async def change_nickname(id: int, nickname: NicknameUpdate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	nickname = await ClientNickname.update(id=id, nickname=nickname)
	if nickname is None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ник не найден")
	return NicknamePublic(**nickname.dict()).dict()


@nicknames_router.delete("/{id}", status_code=status.HTTP_200_OK, description="Удалить ник")
async def delete_nickname(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	nickname_id = await ClientNickname.delete(id)
	if nickname_id is None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ник не найден")
	return {"nickname_id": nickname_id}


@urls_router.get(
	"/{id}", response_model=UrlPublic, status_code=200,
	description="Получить информацию о ссылке по id",
	responses={
		200: {
			"description": "Успешный запрос"
		}
	}
)
async def get_url(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	url = await ClientUrl.get(id)
	if url is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ссылка не найдена")
	return UrlPublic(**url.dict()).dict()


@urls_router.post("/", status_code=status.HTTP_200_OK, description="Создать новую ссылку")
async def create_url(url: UrlCreate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	try:
		url_id = await ClientUrl.create(url)
	except UniqueViolationError:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такая ссылка уже сохранена")
	return {"url_id": url_id}


@urls_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, description="Изменить ссылку")
async def change_url(id: int, url: UrlUpdate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	url = await ClientUrl.update(id=id, url=url)
	if url is None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ссылка не найдена")
	return UrlPublic(**url.dict()).dict()


@urls_router.delete("/{id}", status_code=status.HTTP_200_OK, description="Удалить ссылку")
async def delete_url(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	url_id = await ClientUrl.delete(id)
	if url_id is None:
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ссылка не найдена")
	return {"url_id": url_id}
