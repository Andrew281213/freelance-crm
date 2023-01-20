from pydantic import Field, validator, ValidationError
from enum import Enum
from datetime import datetime, timedelta
from app.base_schemas import CoreModel, IDModelMixin


class OrderStatus(Enum):
	new = 0                 # Новый
	in_work = 1             # В работе
	canceled = 2            # Отменен
	getting_details = 3     # Уточнение деталей
	on_check = 4            # На проверке
	completed = 5           # Завершен


class OrderFileBase(CoreModel):
	filename: str
	upload_ts: float = datetime.now().timestamp()
	is_result: bool = False


class OrderFileCreate(OrderFileBase):
	pass


class OrderFileUpdate(IDModelMixin, OrderFileBase):
	pass


class OrderFileDelete(IDModelMixin):
	pass


class OrderFileInDB(IDModelMixin, OrderFileBase):
	filepath: str


class OrderFilePublic(IDModelMixin):
	filepath: str
	upload_ts: float
	is_result: bool = False


class OrderBase(CoreModel):
	client_id: int
	cost: int
	status: OrderStatus = OrderStatus.new
	create_ts: float = datetime.now().timestamp()
	deadline_ts: float | None = (datetime.now() + timedelta(days=1)).timestamp()
	tz: str | None = None
	input_files: list[OrderFilePublic] = Field(default_factory=list)
	result_files: list[OrderFilePublic] = Field(default_factory=list)
	end_ts: float | None = None
	comment: str | None = None
	spent_hours: int | None = None

	@validator("cost")
	def check_cost(self, val):
		if val <= 0:
			raise ValidationError()

	@validator("spent_hours")
	def check_spent_hours(self, val):
		if val is not None and val <= 0:
			raise ValidationError()


class OrderCreate(OrderBase):
	input_files: list[OrderFileCreate] = Field(default_factory=list)


class OrderUpdate(IDModelMixin, OrderBase):
	input_files: list[OrderFileUpdate] = Field(default_factory=list)
	result_files: list[OrderFileUpdate] = Field(default_factory=list)


class OrderDelete(IDModelMixin):
	pass


class OrderInDB(IDModelMixin, OrderBase):
	input_files: list[OrderFileInDB] = Field(default_factory=list)
	result_files: list[OrderFileInDB] = Field(default_factory=list)


class OrderPublic(IDModelMixin, OrderBase):
	date_str: str
	pass
