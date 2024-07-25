import os
import pymysql
import pymysql.cursors

from dotenv import load_dotenv
from pymysql.constants import CLIENT

load_dotenv()

TEST_HOST = os.getenv("HOST")
TEST_USERID = os.getenv("USERID")
TEST_PASSWORD = os.getenv("PASSWORD")
TEST_DBNAME = os.getenv("DBNAME")


class Connection:
    def __init__(self, host, userid, password, dbname):
        self.host = host
        self.user = userid
        self.password = password
        self.db = dbname
        self.port = 3306
        self.charset = 'utf8'
        self.conn = pymysql.connect(
            host=self.host, user=self.user, password=self.password,
            db=self.db, port=self.port, charset=self.charset, client_flag=CLIENT.MULTI_STATEMENTS)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print('[알림] DB와 성공적으로 연결되었습니다.')

    def __del__(self):
        self.conn.close()
        print('[알림] DB와의 연결을 끊었습니다.')

    def get_connection(self):
        self.conn.ping()
        return self.conn, self.cur


connection = Connection(TEST_HOST, TEST_USERID, TEST_PASSWORD, TEST_DBNAME)
