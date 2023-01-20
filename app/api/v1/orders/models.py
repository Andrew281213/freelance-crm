from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, PrimaryKeyConstraint, TIMESTAMP, Boolean

from app.db import db, metadata
from .schemas import OrderCreate, OrderInDB, OrderChangeCreate, OrderChangeInDB

orders = Table(
	"orders",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("client_id", ForeignKey("clients.id"), nullable=False),
	Column("tz", Text, comment="Текст тз"),
	Column("start_ts", TIMESTAMP, nullable=False, comment="Дата создания заказа"),
	Column("deadline_ts", TIMESTAMP, nullable=False, comment="Дата дедлайна"),
	Column("end_ts", TIMESTAMP, comment="Дата завершения работы"),
	Column("comment", Text, comment="Комментарий к заказу"),
	Column("cost", Integer, nullable=False, comment="Стоимость работы"),
	Column("spent_hours", Integer, comment="Затраченное время"),
	Column("status", Integer, nullable=False, comment="Статус заказа")
)

order_files = Table(
	"order_files",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("filepath", String(255), nullable=False, comment="Путь к файлу"),
	Column("upload_ts", TIMESTAMP, nullable=False, comment="Дата загрузки"),
	Column("is_result", Boolean, comment="Файл относится к результатам?")
)

order_changes_history = Table(
	"order_changes_history",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("order_id", ForeignKey("orders.id"), index=True, comment="Id заказа"),
	Column("text", Text, comment="Текст изменения"),
	Column("type", Integer, nullable=False, comment="Тип изменения"),
	Column("create_ts", TIMESTAMP, nullable=False, comment="Дата создания изменения"),
	Column("status", Integer, nullable=False, comment="Статус заказа")
)

changes_order_files = Table(
	"changes_order_files",
	metadata,
	Column("change_id", ForeignKey("order_changes_history.id"), comment="Id изменения"),
	Column("order_file_id", ForeignKey("order_files.id"), comment="Id файла"),
	PrimaryKeyConstraint("change_id", "order_file_id")
)


class OrderChange:
	@classmethod
	async def create(cls, order_change):
		"""Записывает данные об изменении в бд

		:param OrderChangeCreate order_change: Данные об изменении
		:return: Id изменения
		:rtype: int
		"""
		query = order_changes_history.insert().values(**order_change.dict())
		change_id = await db.execute(query)
		return change_id

	@classmethod
	async def get(cls, id):
		"""Получить информацию об изменении

		:param int id: Id изменения
		:return: Информация об изменении
		:rtype: OrderChangeInDB | None
		"""
		query = order_changes_history.select().where(order_changes_history.c.id == id)
		order_change = await db.fetch_one(query)
		if order_change is not None:
			return OrderChangeInDB(**order_change)

	@classmethod
	async def get_by_order_id(cls, order_id):
		"""Получить список изменений по Id заказа

		:param int order_id: Id заказа
		:return: Список изменений в заказе
		:rtype: list[OrderChangeInDB]
		"""
		query = order_changes_history.select().where(order_changes_history.c.order_id == order_id)
		order_changes = await db.fetch_all(query)
		if len(order_changes) == 0:
			return []
		data = []
		for order_change in order_changes:
			data.append(OrderChangeInDB(**order_change))
		return data


class Order:
	@classmethod
	async def create(cls, order):
		"""Записывает данные о заказе в бд

		:param OrderCreate order: Данные о заказе
		:return: Id заказа из бд
		:rtype: int
		"""
		# TODO: Добавить сохранение файлов
		order.status = order.status.value
		query = orders.insert().values(
			start_ts=datetime.now(), **order.dict()
		)
		order_id = await db.execute(query)
		return order_id

	@classmethod
	async def get(cls, id):
		"""Получает информацию о заказе по id

		:param int id: Id заказа
		:return: Информация о заказе
		:rtype: OrderInDB
		"""
		query = orders.select().where(orders.c.id == id)
		order = await db.fetch_one(query)
		if order is not None:
			order = dict(order)
			return OrderInDB(**order)

	@classmethod
	async def get_all(cls):
		"""Получает данные по всем заказам в базе

		:return: Список с данными о всех заказах
		:rtype: list[OrderInDB]
		"""
		query = orders.select()
		orders_data = await db.fetch_all(query)
		if len(orders_data) == 0:
			return []
		data = []
		for order_item in orders_data:
			order_item = dict(order_item)
			data.append(OrderInDB(**order_item))
		return data

	@classmethod
	async def delete(cls, id):
		"""Удалить заказ из бд

		:param int id: Id заказа
		:return: Id удаленного заказа или None, если заказ не был найден
		:rtype: int | None
		"""
		order = await Order.get(id)
		if order is None:
			return None
		query = orders.delete().where(orders.c.id == id)
		await db.execute(query)
		return id
