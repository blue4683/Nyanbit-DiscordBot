import os
import sys
from dotenv import load_dotenv

from nyanbit.core.db import Connection

sys.path.append('C:/develop_discord_bot')
load_dotenv()

TEST_HOST = os.getenv("HOST")
TEST_USERID = os.getenv("USERID")
TEST_PASSWORD = os.getenv("PASSWORD")
TEST_DBNAME = os.getenv("DBNAME")

test_connection = Connection(
    TEST_HOST, TEST_USERID, TEST_PASSWORD, TEST_DBNAME)

conn, cur = test_connection.get_connection()

sql = open("tests/test.sql").read()
cur.execute(sql)
conn.commit()
conn.close()
