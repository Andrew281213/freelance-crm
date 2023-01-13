import pytest
from fastapi import status
<<<<<<< HEAD
from loguru import logger

from app.api.v1.users import models
=======
>>>>>>> fae9498 (Добавлены тесты пользователей)

users_url = "/api/v1/users"
TIMEOUT = 5


def test_not_auth_to_auth_required(test_client):
	resp = test_client.get(users_url + "/1", timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_401_UNAUTHORIZED, "Не соответствует статус-код"
	resp = test_client.delete(users_url + "/logout", timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_401_UNAUTHORIZED, "Не соответствует статус-код"
	resp = test_client.get(users_url + "/me/", timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_401_UNAUTHORIZED, "Не соответствует статус-код"


@pytest.mark.parametrize("payload,status_code,response_keys", (
		({}, status.HTTP_422_UNPROCESSABLE_ENTITY, None),
		({"username": "test"}, status.HTTP_422_UNPROCESSABLE_ENTITY, None),
		({"password": "test123"}, status.HTTP_422_UNPROCESSABLE_ENTITY, None),
		({"password": "test"}, status.HTTP_422_UNPROCESSABLE_ENTITY, None),
		({"username": "tt", "password": "test123"}, status.HTTP_200_OK, None),
		({"username": "test1", "password": "test123"}, status.HTTP_200_OK, ["user_id"]),
		({"username": "test1", "password": "test12345"}, status.HTTP_409_CONFLICT, None)
))
def test_create_user(test_client, payload, status_code, response_keys):
	resp = test_client.post(users_url, json=payload, timeout=TIMEOUT)
	assert resp.status_code == status_code, "Не соответствует статус-код"
	resp_data = resp.json()
	if response_keys is not None:
		assert list(resp_data.keys()) == response_keys, "Не соответствуют ключи ответа"


def test_good_login_user(test_client):
	payload = {
		"username": "test_login1",
		"password": "test123"
	}
	resp = test_client.post(users_url, json=payload, timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при создании пользователя"
	resp = test_client.post(users_url + "/login", json=payload)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при авторизации"
	resp_data = resp.json()
	assert list(resp_data.keys()) == ["username", "id"], "Не соответствуют ключи ответа"
	assert resp_data.get("username") == payload.get("username"), "Не соответствует ник пользователя"
	assert isinstance(resp_data.get("id"), int), "id пользователя не int"
	assert resp.headers.get("set-cookie", "").find("access_token") > -1, "Не найдено поле jwt токена в заголовках"


@pytest.mark.parametrize("payload,status_code", (
		({"username": "estsdfjksdjl", "password": "fkjsldjfl"}, status.HTTP_401_UNAUTHORIZED),
		({"username": "fkjsldkfjsldf", "password": "11"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
))
def test_bad_login_user(test_client, payload, status_code):
	resp = test_client.post(users_url + "/login", json=payload)
	assert resp.status_code == status_code, "Не соответствует статус-код"


def test_logout_user(test_client):
	payload = {
		"username": "test_logout1",
		"password": "test123"
	}
	resp = test_client.post(users_url, json=payload, timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при создании пользователя"
	resp = test_client.post(users_url + "/login", json=payload)
	headers = resp.headers.get("set-cookie")
	assert headers is not None, "Не созданы куки при авторизации"
	key, val = headers.split(";")[0].split("=")
	headers = {key: val}
	resp = test_client.delete(users_url + "/logout", headers=headers)
	assert resp.status_code == status.HTTP_200_OK
	cookies = []
	for headers in resp.headers.get("set-cookie").split(","):
		if headers.find('=""') == -1:
			continue
		cookie, _ = headers.split(";")
		cookies.append(cookie)
	assert 'access_token_cookie=""' in cookies, "Куки авторизации не удалены"


def test_get_me(test_client):
	payload = {
		"username": "test_get_me1",
		"password": "test123"
	}
	resp = test_client.post(users_url, json=payload, timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при создании пользователя"
	resp = test_client.post(users_url + "/login", json=payload)
	headers = resp.headers.get("set-cookie")
	assert headers is not None, "Не созданы куки при авторизации"
	key, val = headers.split(";")[0].split("=")
	headers = {key: val}
	resp = test_client.get(users_url + "/me/", headers=headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при запросе данных о текущем пользователе"
	resp_data = resp.json()
	assert resp_data.get("username") == payload.get("username"), "Не соответствует ник пользователя"
	assert isinstance(resp_data.get("id"), int), "id пользователя не int"

