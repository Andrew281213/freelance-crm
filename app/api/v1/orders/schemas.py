from datetime import datetime, timedelta
from enum import Enum

from pydantic import Field, validator, ValidationError

from app.base_schemas import CoreModel, IDModelMixin


class OrderStatus(Enum):
	new = 0  # Новый
	in_work = 1  # В работе
	canceled = 2  # Отменен
	getting_details = 3  # Уточнение деталей
	on_check = 4  # На проверке
	completed = 5  # Завершен


class ChangeType(Enum):
	change_status = 0
	add_files = 1
	remove_files = 2
	change_order = 3


class OrderFileBase(CoreModel):
	filename: str
	is_result: bool = False


class OrderFileCreate(CoreModel):
	order_id: int
	filepath: str
	is_result: bool = False


class OrderFileUpdate(IDModelMixin, OrderFileBase):
	pass


class OrderFileDelete(IDModelMixin):
	pass


class OrderFileInDB(IDModelMixin):
	filepath: str
	upload_ts: datetime
	is_result: bool = False


class OrderFilePublic(IDModelMixin, OrderFileBase):
	filepath: str
	upload_ts: datetime
	upload_str: datetime

	class Config:
		schema_extra = {
			"example": {
				"filename": "test.png",
				"filepath": "dir1/dir2/test.png",
				"upload_ts": 1674923175,
				"upload_str": "28.01.2023 16:26",
				"is_result": False
			},
			"properties": {
				"id": {
					"title": "ID файла заказа",
					"type": "integer"
				},
				"filename": {
					"title": "Название файла",
					"type": "string"
				},
				"filepath": {
					"title": "Путь к файлу",
					"type": "string"
				},
				"upload_ts": {
					"title": "Timestamp времени загрузки файла",
					"type": "number"
				},
				"upload_str": {
					"title": "Дата и время загрузки файла в виде строки",
					"type": "string"
				},
				"is_result": {
					"title": "Файл относится к результатам работы?",
					"type": "boolean"
				}
			}
		}


class OrderChangeBase(CoreModel):
	order_id: int
	type: ChangeType
	status: OrderStatus
	text: str | None = None


class OrderChangeCreate(OrderChangeBase):
	pass


class OrderChangeInDB(IDModelMixin, OrderChangeBase):
	create_ts: datetime


class OrderChangePublic(IDModelMixin, OrderChangeBase):
	create_ts: datetime
	create_date: str


class OrderBase(CoreModel):
	client_id: int
	cost: int
	status: OrderStatus = OrderStatus.new
	deadline_ts: datetime | None = (datetime.now() + timedelta(days=1))
	tz: str | None = None
	end_ts: datetime | None = None
	comment: str | None = None
	spent_hours: int | None = None

	@validator("cost")
	def check_cost(cls, val):
		if val <= 0:
			raise ValidationError()
		return val

	@validator("spent_hours")
	def check_spent_hours(cls, val):
		if val is not None and val <= 0:
			raise ValidationError()
		return val


class OrderCreate(OrderBase):
	class Config:
		schema_extra = {
			"example": {
				"client_id": 1,
				"cost": 500,
				"status": 0,
				"deadline_ts": 1674327110.422097,
				"tz": "Сделать парсер...",
				"input_files": [],
				"result_files": [],
				"end_ts": 1674327110.422097,
				"comment": "Хороший получился парсер...",
				"spent_hours": None
			}
		}


class OrderUpdate(IDModelMixin, OrderBase):
	pass


class OrderDelete(IDModelMixin):
	pass


class OrderInDB(IDModelMixin, OrderBase):
	start_ts: datetime
	input_files: list[OrderFileInDB] = Field(default_factory=list)
	result_files: list[OrderFileInDB] = Field(default_factory=list)


class OrderPublic(IDModelMixin, OrderBase):
	input_files: list[int] = Field(default_factory=list)
	result_files: list[int] = Field(default_factory=list)
	start_ts: datetime
	start_str: str
	deadline_str: str
	ends_str: str | None = None
