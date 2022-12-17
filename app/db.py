import os
from databases import Database
from dotenv import load_dotenv
import sqlalchemy


load_dotenv()

db = Database(os.environ.get("DATABASE_URL"))
metadata = sqlalchemy.MetaData()
