import os

import sqlalchemy
from databases import Database
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("TESTING"):
	db = Database(os.environ.get("TESTING_DATABASE_URL"))
else:
	db = Database(os.environ.get("DATABASE_URL"))
metadata = sqlalchemy.MetaData()
