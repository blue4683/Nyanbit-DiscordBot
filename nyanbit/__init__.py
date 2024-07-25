import os
import sys
from dotenv import load_dotenv

from nyanbit.core.db import Connection

sys.path.append('C:/develop_discord_bot')
load_dotenv()

HOST = os.getenv("SERVER_HOST")
USERID = os.getenv("SERVER_USERID")
PASSWORD = os.getenv("SERVER_PASSWORD")
DBNAME = os.getenv("SERVER_DBNAME")

connection = Connection(HOST, USERID, PASSWORD, DBNAME)
