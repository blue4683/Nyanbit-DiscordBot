import os
from dotenv import load_dotenv

from tests.core.db import Connection

load_dotenv()

TEST_HOST = os.getenv("HOST")
TEST_USERID = os.getenv("USERID")
TEST_PASSWORD = os.getenv("PASSWORD")
TEST_DBNAME = os.getenv("DBNAME")

test_connection = Connection(
    TEST_HOST, TEST_USERID, TEST_PASSWORD, TEST_DBNAME)
