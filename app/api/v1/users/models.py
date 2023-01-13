from sqlalchemy import Table, Column, Integer, String

from app.db import db, metadata
from .schemas import UserCreate, UserInDB


# TODO: добавить ограничение на минимальную длину ника

users = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column(
		"username", String(length=32), index=True, unique=True,
		nullable=False, comment="Имя пользователя"
	),
	Column(
		"password", String(), nullable=False, comment="Пароль пользователя"
	)
)


class User:
	@classmethod
	async def create(cls, user):
		"""Записывает данные о новом пользователе в бд

		:param UserCreate user: Данные о пользователе
		:return: ID пользователя в бд
		:rtype: int
		"""
		query = users.insert().values(**user.dict())
		user_id = await db.execute(query)
		return user_id

	@classmethod
	async def get(cls, id):
		"""Получает информацию о пользователе из бд

		:param int id: ID пользователя
		:return: Информация о пользователе
		:rtype: UserInDB
		"""
		query = users.select().where(users.c.id == id)
		user = await db.fetch_one(query)
		if user is not None:
			return UserInDB(**user)
		return None

	@classmethod
	async def get_by_username(cls, username):
		"""Получает информацию о пользователе из бд

		:param str username: Имя пользователя
		:return: Информация о пользователе
		:rtype: UserInDB
		"""
		query = users.select().where(users.c.username == username)
		user = await db.fetch_one(query)
		if user is not None:
			return UserInDB(**user)
		return None
