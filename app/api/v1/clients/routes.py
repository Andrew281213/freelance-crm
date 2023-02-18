from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from fastapi import APIRouter, Depends, HTTPException, status

from .models import ClientUrl, ClientNickname, Client
from .schemas import UrlCreate, NicknameCreate, UrlPublic, NicknamePublic, NicknameUpdate, UrlUpdate, ClientPublic, \
	ClientCreate
from ..users.utils import get_current_user

base_responses = {
	status.HTTP_200_OK: {"description": "Успешный запрос"},
	status.HTTP_404_NOT_FOUND: {"description": "Страница не найдена"},
	status.HTTP_401_UNAUTHORIZED: {
		"description": "Ошибка авторизации",
		"content": {
			"application/json": {
				"example": {"detail": "Not authenticated"}
			}
		}
	},
}

nicknames_router = APIRouter(responses=base_responses, prefix="/nicknames")
urls_router = APIRouter(responses=base_responses, prefix="/urls")
clients_router = APIRouter(responses=base_responses)


@nicknames_router.get(
	"/{id}", response_model=NicknamePublic, status_code=200,
	description="Получить информацию о нике по id",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_404_NOT_FOUND: {
			"description": "Ник клиента с таким id не найден",
			"content": {
				"application/json": {
					"example": {"detail": "Ник не найден"}
				}
			}
		}
	},
)
async def get_nickname(id: int):
	nickname = await ClientNickname.get(id)
	if nickname is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Ник не найден"
		)
	return NicknamePublic(**nickname.dict()).dict()


@nicknames_router.post(
	"/", status_code=status.HTTP_200_OK,
	description="Создать новый ник",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: {
			"content": {
				"application/json": {
					"example": {"nickname_id": 1}
				}
			}
		},
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_409_CONFLICT: {
			"description": "Такой ник уже зарегистрирован",
			"content": {
				"application/json": {
					"example": {"detail": "Такой ник уже зарегистрирован"}
				}
			}
		}
	},
)
async def create_nickname(nickname: NicknameCreate):
	try:
		nickname_id = await ClientNickname.create(nickname)
	except UniqueViolationError:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT, detail="Такой ник уже зарегистрирован"
		)
	return {"nickname_id": nickname_id}


@nicknames_router.put(
	"/{id}", status_code=status.HTTP_202_ACCEPTED,
	response_model=NicknamePublic,
	description="Изменить ник",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_202_ACCEPTED: base_responses[status.HTTP_200_OK],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_400_BAD_REQUEST: {
			"description": "Неверный запрос",
			"content": {
				"application/json": {
					"example": {"detail": "Ник не найден"}
				}
			}
		}
	},
)
async def change_nickname(id: int, nickname: NicknameUpdate):
	nickname = await ClientNickname.update(id=id, nickname=nickname)
	if nickname is None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Ник не найден"
		)
	return NicknamePublic(**nickname.dict()).dict()


@nicknames_router.delete(
	"/{id}", status_code=status.HTTP_200_OK,
	description="Удалить ник",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: {
			"content": {
				"application/json": {
					"example": {"nickname_id": 1}
				}
			}
		},
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_400_BAD_REQUEST: {
			"description": "Неверный запрос",
			"content": {
				"application/json": {
					"example": {"detail": "Ник не найден"}
				}
			}
		}
	},
)
async def delete_nickname(id: int):
	nickname_id = await ClientNickname.delete(id)
	if nickname_id is None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Ник не найден"
		)
	return {"nickname_id": nickname_id}


@urls_router.get(
	"/{id}", response_model=UrlPublic, status_code=200,
	description="Получить информацию о ссылке по id",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_404_NOT_FOUND: {
			"description": "Страница не найдена",
			"content": {
				"application/json": {
					"example": {"detail": "Ссылка не найдена"}
				}
			}
		}
	},
)
async def get_url(id: int):
	url = await ClientUrl.get(id)
	if url is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Ссылка не найдена"
		)
	return UrlPublic(**url.dict()).dict()


@urls_router.post(
	"/", status_code=status.HTTP_200_OK,
	description="Создать новую ссылку",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: {
			"content": {
				"application/json": {
					"example": {"nickname_id": 1}
				}
			}
		},
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_409_CONFLICT: {
			"description": "Такая ссылка уже сохранена",
			"content": {
				"application/json": {
					"example": {"detail": "Такая ссылка уже сохранена"}
				}
			}
		}
	},
)
async def create_url(url: UrlCreate):
	try:
		url_id = await ClientUrl.create(url)
	except UniqueViolationError:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT, detail="Такая ссылка уже сохранена"
		)
	return {"url_id": url_id}


@urls_router.put(
	"/{id}", status_code=status.HTTP_202_ACCEPTED,
	description="Изменить ссылку",
	dependencies=[Depends(get_current_user)],
	response_model=UrlPublic,
	responses={
		status.HTTP_200_OK: {
			"content": {
				"application/json": {
					"example": {"nickname_id": 1}
				}
			}
		},
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_400_BAD_REQUEST: {
			"description": "Неверный запрос",
			"content": {
				"application/json": {
					"example": {"detail": "Ссылка не найдена"}
				}
			}
		}
	},
)
async def change_url(id: int, url: UrlUpdate):
	url = await ClientUrl.update(id=id, url=url)
	if url is None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Ссылка не найдена"
		)
	return UrlPublic(**url.dict()).dict()


@urls_router.delete(
	"/{id}", status_code=status.HTTP_200_OK,
	description="Удалить ссылку",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: {
			"content": {
				"application/json": {
					"example": {"url_id": 1}
				}
			}
		},
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_400_BAD_REQUEST: {
			"description": "Неверный запрос",
			"content": {
				"application/json": {
					"example": {"detail": "Ссылка не найдена"}
				}
			}
		}
	},
)
async def delete_url(id: int):
	url_id = await ClientUrl.delete(id)
	if url_id is None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Ссылка не найдена"
		)
	return {"url_id": url_id}


@clients_router.get(
	"/{id}", response_model=ClientPublic, status_code=status.HTTP_200_OK,
	description="Получить информацию о клиенте по id",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_404_NOT_FOUND: {
			"description": "Страница не найдена",
			"content": {
				"application/json": {
					"example": {"detail": "Клиент не найден"}
				}
			}
		}
	},
)
async def get_client(id: int):
	client = await Client.get(id)
	if client is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найдена"
		)
	return ClientPublic(**client.dict()).dict()


@clients_router.post(
	"/", status_code=status.HTTP_200_OK,
	description="Создать нового клиента",
	dependencies=[Depends(get_current_user)],
	responses={
		status.HTTP_200_OK: base_responses[status.HTTP_200_OK],
		status.HTTP_401_UNAUTHORIZED: base_responses[status.HTTP_401_UNAUTHORIZED],
		status.HTTP_409_CONFLICT: {
			"description": "Такой клиент уже существует",
			"content": {
				"application/json": {
					"example": {"detail": "Такой клиент уже есть"}
				}
			}
		},
		status.HTTP_400_BAD_REQUEST: {
			"description": "Неверный запрос",
			"content": {
				"application/json": {
					"example": {"detail": "Неверно указаны id ников или ссылок"}
				}
			}
		}
	},
)
async def create_client(client: ClientCreate):
	try:
		client_id = await Client.create(client)
	except UniqueViolationError:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT, detail="Такой клиент уже есть"
		)
	except ForeignKeyViolationError:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Неверно указаны id ников или ссылок"
		)
	return {"client_id": client_id}
