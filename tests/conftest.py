<<<<<<< HEAD

import asyncio
=======
>>>>>>> fae9498 (Добавлены тесты пользователей)
import os

os.environ["TESTING"] = "True"

<<<<<<< HEAD
import databases
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from loguru import logger
from app import db
=======
import pytest
from fastapi.testclient import TestClient
from loguru import logger
>>>>>>> fae9498 (Добавлены тесты пользователей)
from app.main import app
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import drop_database, create_database


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


@pytest.fixture()
def test_client(temp_db):
	with TestClient(app) as client:
		yield client
