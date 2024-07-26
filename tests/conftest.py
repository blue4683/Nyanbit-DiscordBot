import pytest
from tests import test_connection


@pytest.fixture(scope='module')
def connection():
    conn, cur = test_connection.get_connection()

    sql = open("tests/test.sql").read()
    cur.execute(sql)
    conn.commit()
    conn.close()

    return test_connection
