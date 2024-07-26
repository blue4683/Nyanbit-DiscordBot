import os
from dotenv import load_dotenv

from nyanbit.core.db import Connection

load_dotenv()

HOST = os.getenv("SERVER_HOST")
USERID = os.getenv("SERVER_USERID")
PASSWORD = os.getenv("SERVER_PASSWORD")
DBNAME = os.getenv("SERVER_DBNAME")

connection = Connection(HOST, USERID, PASSWORD, DBNAME)
