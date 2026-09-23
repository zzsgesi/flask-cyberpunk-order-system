import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import cursors

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    setsession=[],
    ping=1,
    host="127.0.0.1", port=3306, user="root", password="123369", charset="utf8mb4", db="flask_project_db"
)


def fetch_one(sql, params):
    conn = pool.connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        return result
    finally:
        conn.close()


def fetch_all(sql, params):
    conn = pool.connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        return result
    finally:
        conn.close()


def create(sql, params):
    conn = pool.connection()
    try:
        with conn.cursor(cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
        conn.commit()
    finally:
        conn.close()
        return cursor.lastrowid


def execute(sql, params):
    conn = pool.connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()
    finally:
        conn.close()
