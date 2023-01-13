import os

from starlette import status

os.environ["TESTING"] = "True"

import pytest
from fastapi.testclient import TestClient
from loguru import logger
from app.main import app
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import drop_database, create_database


users_url = "/api/v1/users"


# @pytest.fixture(scope="session")
@pytest.fixture(scope="module")
def temp_db():
	try:
		logger.info("Creating test db")
		create_database(os.environ.get("TESTING_DATABASE_URL"))
		# drop_database(os.environ.get("TESTING_DATABASE_URL"))
		# create_database(os.environ.get("TESTING_DATABASE_URL"))
		base_dir = os.path.dirname(os.path.dirname(__file__))
		logger.info(f"{base_dir=}")
		alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
		logger.info("Creating tables")
		command.upgrade(alembic_cfg, "head")
		yield os.environ.get("TESTING_DATABASE_URL")
	finally:
		logger.info("Removing test db")
		drop_database(os.environ.get("TESTING_DATABASE_URL"))


@pytest.fixture(scope="module")
def test_client(temp_db):
	with TestClient(app) as client:
		yield client


@pytest.fixture(scope="module")
def auth_headers(test_client):
	logger.info("Создаю пользователя")
	payload = {
		"username": "test_logout1",
		"password": "test123"
	}
	resp = test_client.post(users_url, json=payload)
	assert resp.status_code == status.HTTP_200_OK, "Не соответствует статус-код при создании пользователя"
	resp = test_client.post(users_url + "/login", json=payload)
	headers = resp.headers.get("set-cookie")
	assert headers is not None, "Не созданы куки при авторизации"
	key, val = headers.split(";")[0].split("=")
	headers = {key: val}
	yield headers
