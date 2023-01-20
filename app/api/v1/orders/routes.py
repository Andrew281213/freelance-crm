from asyncpg import ForeignKeyViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT

from .models import Order
from .schemas import OrderCreate, OrderPublic

DATETIME_FORMAT = "%d.%m.%Y %H:%M"

base_responses = {
	status.HTTP_200_OK: {"description": "Успешный запрос"},
	status.HTTP_404_NOT_FOUND: {"description": "Страница не найдена"},
	status.HTTP_400_BAD_REQUEST: {"description": "Неверный запрос"},
	status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Неверно указаны данные"}
}

orders_router = APIRouter(responses=base_responses)
order_files_router = APIRouter(responses=base_responses)


@orders_router.get(
	"/", response_model=list[OrderPublic], status_code=status.HTTP_200_OK,
	description="Получить список заказов",

)
async def get_orders(jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	orders = await Order.get_all()
	data = []
	for order in orders:
		start_str = order.start_ts.strftime(DATETIME_FORMAT)
		deadline_str = order.deadline_ts.strftime(DATETIME_FORMAT)
		if order.end_ts is not None:
			end_str = order.end_ts.strftime(DATETIME_FORMAT)
		else:
			end_str = None
		data.append(
			OrderPublic(
				start_str=start_str, deadline_str=deadline_str, end_str=end_str, **order.dict()
			)
		)
	return data


@orders_router.get(
	"/{id}", response_model=OrderPublic, status_code=status.HTTP_200_OK,
	description="Получить информацию о заказе по id"
)
async def get_order(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	order = await Order.get(id)
	if order is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Заказ не найден"
		)
	start_str = order.start_ts.strftime(DATETIME_FORMAT)
	deadline_str = order.deadline_ts.strftime(DATETIME_FORMAT)
	if order.end_ts is not None:
		end_str = order.end_ts.strftime(DATETIME_FORMAT)
	else:
		end_str = None
	return OrderPublic(
		start_str=start_str, deadline_str=deadline_str, end_str=end_str, **order.dict()
	)


@orders_router.post(
	"/", status_code=status.HTTP_200_OK,
	description="Создать новый заказ. Возвращает id заказа"
)
async def create_order(order: OrderCreate, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	try:
		order_id = await Order.create(order)
	except ForeignKeyViolationError:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Клиент не найден"
		)
	return {"order_id": order_id}


@orders_router.delete(
	"/{id}", status_code=status.HTTP_200_OK,
	description="Удалить заказ"
)
async def delete_order(id: int, jwt: AuthJWT = Depends()):
	jwt.jwt_required()
	order_id = await Order.delete(id)
	if order_id is None:
		return HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Заказ не найден"
		)
	return {"order_id": order_id}
