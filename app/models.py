from .db import db, metadata
from sqlalchemy import Table, Column, Integer, String

users = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, index=True),
	Column("first_name", String),
	Column("last_name", String)
)


class User:
	@classmethod
	async def get(cls, idx):
		query = users.select().where(users.c.id == idx)
		user = await db.fetch_one(query)
		return user

	@classmethod
	async def create(cls, **user):
		query = users.insert().values(**user)
		user_id = await db.execute(query)
		return user_id
