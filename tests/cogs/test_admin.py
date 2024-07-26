from dotenv import load_dotenv
import os
import pymysql
import pytest

load_dotenv()
TEST_ID = os.getenv("TEST_ID")
TEST_NAME = os.getenv("TEST_NAME")


def test_add(connection):
    _, cur = connection.get_connection()

    sql = 'SELECT user_id, user_name, is_admin, nyanbit FROM userinfo WHERE user_id = %s;'
    cur.execute(sql, TEST_ID)
    result = cur.fetchone()

    assert result['user_id'] == TEST_ID
    assert result['user_name'] == TEST_NAME
    assert result['is_admin'] == 0
    assert result['nyanbit'] == 0


def test_add_duplicated(connection):
    with pytest.raises(pymysql.err.IntegrityError):
        conn, cur = connection.get_connection()

        sql = 'INSERT INTO userinfo (user_id, user_name, is_admin, nyanbit) VALUES (%s, %s, %s, %s);'
        cur.execute(sql, (TEST_ID, TEST_NAME, 0, 0))
        conn.commit()


def test_set_admin(connection):
    conn, cur = connection.get_connection()

    sql = 'UPDATE userinfo SET is_admin = %s WHERE user_id = %s;'
    cur.execute(sql, (1, TEST_ID))
    conn.commit()

    sql = 'SELECT is_admin FROM userinfo WHERE user_id = %s;'
    cur.execute(sql, TEST_ID)
    result = cur.fetchone()
    conn.close()

    assert result['is_admin'] == 1


def test_give(connection):
    conn, cur = connection.get_connection()

    sql = 'SELECT nyanbit FROM userinfo WHERE user_id = %s'
    cur.execute(sql, TEST_ID)
    result = cur.fetchone()

    sql = 'UPDATE userinfo SET nyanbit = %s WHERE user_id = %s'
    cur.execute(sql, (result['nyanbit'] + 1, TEST_ID))
    conn.commit()

    sql = 'SELECT nyanbit FROM userinfo WHERE user_id = %s;'
    cur.execute(sql, TEST_ID)
    result = cur.fetchone()
    conn.close()

    assert result['nyanbit'] == 1
