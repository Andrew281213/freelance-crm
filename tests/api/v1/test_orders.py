import pytest
from fastapi import status


orders_url = "/api/v1/orders"
TIMEOUT = 5


def test_get_all_orders_without_auth(test_client):
	resp = test_client.get(orders_url)
	assert resp.status_code == status.HTTP_401_UNAUTHORIZED, "Должен быть доступ только после авторизации"
	assert list(resp.json().keys()) == ["error"]


def tset_get_all_orders_with_auth(test_client, auth_headers):
	resp = test_client.get(orders_url, headers=auth_headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код после авторизации"
	resp_data = resp.json()
	assert resp_data == [], "Массив должен быть пустым"


@pytest.mark.parametrize("payload, status_code", (
		({"client_id": 1, "cost": 500, "status": 0}, status.HTTP_400_BAD_REQUEST),
		({"cost": 500, "status": 0}, status.HTTP_422_UNPROCESSABLE_ENTITY),
		({"client_id": 1, "cost": -100, "status": 0}, status.HTTP_422_UNPROCESSABLE_ENTITY),
		({"cost": -1, "status": 0}, status.HTTP_422_UNPROCESSABLE_ENTITY),
		({"client_id": 1, "status": 0}, status.HTTP_422_UNPROCESSABLE_ENTITY),
		({"status": 0}, status.HTTP_422_UNPROCESSABLE_ENTITY)
))
def test_wrong_create_order(test_client, auth_headers, payload, status_code):
	resp = test_client.post(orders_url, headers=auth_headers, json=payload)
	assert resp.status_code == status_code, "Не соответствует статус-код создания заказа"


def test_good_create_order(test_client, auth_headers):
	payload = {
		"client_id": 1,
		"cost": 500,
		"status": 0
	}
	client_payload = {
		"fio": "test1"
	}
	resp = test_client.post("/api/v1/clients", json=client_payload, headers=auth_headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код создания клиента"
	resp = test_client.post(orders_url, headers=auth_headers, json=payload)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код создания заказа"
	resp_data = resp.json()
	assert list(resp_data.keys()) == ["order_id"], "Ключи ответа не соответствуют необходимым"
	assert isinstance(resp_data.get("order_id"), int), "Id заказа не int"


def test_get_orders(test_client, auth_headers):
	payload = {
		"client_id": 1,
		"cost": 500,
		"status": 0
	}
	client_payload = {
		"fio": "test1"
	}
	resp = test_client.post("/api/v1/clients", json=client_payload, headers=auth_headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код создания клиента"
	resp = test_client.post(orders_url, headers=auth_headers, json=payload)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код создания заказа"
	order_id = resp.json().get("order_id")
	resp = test_client.get(orders_url + "/" + str(order_id), headers=auth_headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код получения заказа по id"
	resp_data = resp.json()
	assert resp_data.get("client_id") == payload.get("client_id"), "Не соответствует id клиента"
	assert resp_data.get("cost") == payload.get("cost"), "Не соответствует стоимость заказа"
	assert resp_data.get("status") == payload.get("status"), "Не соответствует статус заказа"
	resp = test_client.get(orders_url, headers=auth_headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код получения списка заказов"
	resp_data = resp.json()
	assert len(resp_data) > 0, "Кол-во заказов должно быть > 0"
	order = None
	for order in resp_data:
		if order.get("id") == order_id:
			break
	assert order is not None and order.get("id") == order_id, "Не найден созданный заказ"
	assert order.get("client_id") == payload.get("client_id"), "Не соответствует id клиента в списке заказов"
	assert order.get("cost") == payload.get("cost"), "Не соответствует стоимость заказа в списке заказов"
	assert order.get("status") == payload.get("status"), "Не соответствует статус заказа в списке заказов"
