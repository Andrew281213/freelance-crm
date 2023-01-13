import pytest
from fastapi import status

nicknames_url = "/api/v1/clients/nicknames/"
TIMEOUT = 5


@pytest.mark.parametrize("payload,status_code,response_keys", (
		({"nickname": "tt"}, status.HTTP_200_OK, ["nickname_id"]),
		({"nickname": "tt1"}, status.HTTP_200_OK, ["nickname_id"]),
		({"nickname": "tt"}, status.HTTP_409_CONFLICT, None)
))
def test_create_nickname(test_client, auth_headers, payload, status_code, response_keys):
	resp = test_client.post(nicknames_url, json=payload, headers=auth_headers)
	assert resp.status_code == status_code, "Не соответствует статус-код ответа"
	if response_keys is not None:
		assert list(resp.json().keys()) == response_keys, "Не соответствуют ключи ответа"
