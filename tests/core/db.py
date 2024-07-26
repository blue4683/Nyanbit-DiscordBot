import pymysql
import pymysql.cursors

from pymysql.constants import CLIENT


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
        print('[테스트] DB와 성공적으로 연결되었습니다.')

    def __del__(self):
        self.conn.close()
        print('[테스트] DB와의 연결을 끊었습니다.')

    def get_connection(self):
        self.conn.ping()
        return self.conn, self.cur
