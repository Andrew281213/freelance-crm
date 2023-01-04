from asyncpg import UniqueViolationError
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, PrimaryKeyConstraint

from app.db import db, metadata
from .schemas import NicknameInDB, NicknameCreate, NicknameUpdate, UrlCreate, UrlInDB, UrlUpdate,\
	ClientCreate, ClientInDB, ClientUpdate

clients_nicknames = Table(
	"clients_nicknames",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("nickname", String(length=64), index=True, unique=True, nullable=False, comment="Ник клиента")
)

clients_urls = Table(
	"clients_urls",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("url", String(length=255), unique=True, nullable=False, comment="Ссылка на страницу клиента")
)

clients = Table(
	"clients",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("nickname", String(length=64), index=True, unique=True, nullable=False, comment="Ник клиента"),
	Column("comment", Text, nullable=True, comment="Комментарий")
)

clients_clients_nicknames = Table(
	"clients_clients_nicknames",
	metadata,
	Column("client_id", Integer, ForeignKey("clients.id"), nullable=False),
	Column("nickname_id", Integer, ForeignKey("clients_nicknames.id"), nullable=False),

	PrimaryKeyConstraint("client_id", "nickname_id")
)


clients_clients_urls = Table(
	"client_client_urls",
	metadata,
	Column("client_id", Integer, ForeignKey("clients.id"), nullable=False),
	Column("url_id", Integer, ForeignKey("clients_urls.id"), nullable=False),

	PrimaryKeyConstraint("client_id", "url_id")
)


class ClientNickname:
	@classmethod
	async def create(cls, nickname):
		"""Записывает ник клиента в бд

		:param NicknameCreate nickname: Данные о нике клиента
		:return: ID ника из бд
		:rtype: int
		"""
		query = clients_nicknames.insert().values(**nickname.dict())
		nickname_id = await db.execute(query)
		return nickname_id

	@classmethod
	async def get(cls, id):
		"""Получает информацию о нике из бд

		:param int id: ID ника
		:return: Информация о нике
		:rtype: NicknameInDB
		"""
		query = clients_nicknames.select().where(clients_nicknames.c.id == id)
		nickname = await db.fetch_one(query)
		if nickname is not None:
			return NicknameInDB(**nickname)
		return None

	@classmethod
	async def get_by_nickname(cls, nickname):
		"""Получает информацию о нике из бд

		:param str nickname: Имя пользователя
		:return: Информация о нике клиента
		:rtype: NicknameInDB
		"""
		query = clients_nicknames.select().where(clients_nicknames.c.username == nickname)
		nickname = await db.fetch_one(query)
		if nickname is not None:
			return NicknameInDB(**nickname)
		return None

	@classmethod
	async def update(cls, id, nickname):
		"""Обновляет информацию о нике в бд

		:param int id: Id ника
		:param NicknameUpdate nickname: Новые данные о нике
		:return: Информация о нике клиента
		:rtype: NicknameInDB | None
		"""
		old_data = await ClientNickname.get(id)
		if old_data is None:
			return None
		if nickname.nickname != old_data.nickname:
			query = clients_nicknames.update().\
				where(clients_nicknames.c.id == id).\
				values(nickname=nickname.nickname)
			await db.execute(query)
		return await ClientNickname.get(id)

	@classmethod
	async def delete(cls, id):
		"""Удалить ник

		:param int id: Id ника
		:return: Id удаленного ника или None, если ник не найден
		:rtype: int | None
		"""
		nickname = await ClientNickname.get(id)
		if nickname is None:
			return None
		query = clients_nicknames.delete().where(clients_nicknames.c.id == id)
		await db.execute(query)
		return id


class ClientUrl:
	@classmethod
	async def create(cls, url):
		"""Записывает ссылку на клиента в бд

		:param UrlCreate url: Данные о ссылке клиента
		:return: ID ссылки из бд
		:rtype: int
		"""
		query = clients_urls.insert().values(**url.dict())
		url_id = await db.execute(query)
		return url_id

	@classmethod
	async def get(cls, id):
		"""Получает информацию о ссылке из бд

		:param int id: ID ссылки
		:return: Информация о ссылке
		:rtype: UrlInDB
		"""
		query = clients_urls.select().where(clients_urls.c.id == id)
		url = await db.fetch_one(query)
		if url is not None:
			return UrlInDB(**url)
		return None

	@classmethod
	async def get_by_url(cls, url):
		"""Получает информацию о ссылке из бд

		:param str url: Ссылка на страницу клиента
		:return: Информация о ссылке
		:rtype: UrlInDB
		"""
		query = clients_urls.select().where(clients_urls.c.url == url)
		url = await db.fetch_one(query)
		if url is not None:
			return NicknameInDB(**url)
		return None

	@classmethod
	async def update(cls, id, url):
		"""Обновляет информацию о ссылке в бд

		:param int id: Id ссылки
		:param UrlUpdate url: Новые данные о ссылке
		:return: Информация о ссылке клиента
		:rtype: UrlInDB | None
		"""
		old_data = await ClientUrl.get(id)
		if old_data is None:
			return None
		if url.url != old_data.url:
			query = clients_urls.update(). \
				where(clients_urls.c.id == id). \
				values(url=url.url)
			await db.execute(query)
		return await ClientUrl.get(id)

	@classmethod
	async def delete(cls, id):
		"""Удалить ссылку

		:param int id: Id ссылки
		:return: Id удаленной ссылки или None, если ссылка не найдена
		:rtype: int | None
		"""
		url = await ClientUrl.get(id)
		if url is None:
			return None
		query = clients_urls.delete().where(clients_urls.c.id == id)
		await db.execute(query)
		return id


class Client:
	@classmethod
	async def create(cls, client):
		"""Записывает данные о новом клиенте

		:param ClientCreate client: Данные о клиенте
		:return: Id клиента в бд
		:rtype: int
		"""
		async with db.transaction():
			nickname_ids = []
			if client.nicknames is not None and len(client.nicknames) > 0:
				for nickname in client.nicknames:
					try:
						nickname_id = await ClientNickname.create(NicknameCreate(nickname=nickname))
						if nickname_id is not None:
							nickname_ids.append(nickname_id)
					except UniqueViolationError:
						continue
			url_ids = []
			if client.urls is not None and len(client.urls) > 0:
				for url in client.urls:
					try:
						url_id = await ClientUrl.create(UrlCreate(url=url))
						if url_id is not None:
							url_ids.append(url_id)
					except UniqueViolationError:
						continue
			query = clients.insert().values(nickname=client.nickname, comment=client.comment)
			client_id = await db.execute(query)
			# TODO: добавить проверку на существование ника
			for nickname_id in nickname_ids:
				query = clients_clients_nicknames.insert().values(client_id=client_id, nickname_id=nickname_id)
				await db.execute(query)
			for url_id in url_ids:
				query = clients_clients_urls.insert().values()
				await db.execute(query)
			return client_id
