import pytest
from fastapi import status

users_url = "/api/v1/users"
TIMEOUT = 5


def test_not_auth_to_auth_required(test_client):
	resp = test_client.get(users_url + "/1", timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_401_UNAUTHORIZED, "Не соответствует статус-код получения по id"
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
	resp = test_client.post(users_url + "/token", data=payload)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при авторизации"
	resp_data = resp.json()
	assert list(resp_data.keys()).sort() == ["access_token", "token_type"].sort(), "Не соответствуют ключи ответа"


@pytest.mark.parametrize("payload,status_code", (
		({"username": "estsdfjksdjl", "password": "fkjsldjfl3123"}, status.HTTP_401_UNAUTHORIZED),
		({"username": "fkjsldkfjsldf", "password": "11"}, status.HTTP_401_UNAUTHORIZED)
))
def test_bad_login_user(test_client, payload, status_code):
	resp = test_client.post(users_url + "/token", data=payload)
	assert resp.status_code == status_code, "Не соответствует статус-код: " + str(resp.status_code) + resp.text


def test_get_me(test_client):
	payload = {
		"username": "test_get_me1",
		"password": "test123"
	}
	resp = test_client.post(users_url, json=payload, timeout=TIMEOUT)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при создании пользователя"
	resp = test_client.post(users_url + "/token", data=payload)
	resp_data = resp.json()
	headers = {
		"Authorization": f"{resp_data['token_type']} {resp_data['access_token']}"
	}
	resp = test_client.get(users_url + "/me/", headers=headers)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при запросе данных о текущем пользователе"
	resp_data = resp.json()
	assert resp_data.get("username") == payload.get("username"), "Не соответствует ник пользователя"
	assert isinstance(resp_data.get("id"), int), "id пользователя не int"
