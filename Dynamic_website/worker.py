import redis
import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import cursors
import time

db_pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    setsession=[],
    ping=1,
    host="127.0.0.1", port=3306, user="root", password="123369", charset="utf8mb4", db="flask_project_db"
)

pool = redis.ConnectionPool(max_connections=100)


def fetch_all(sql, params):
    conn = db_pool.connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        return result
    finally:
        conn.close()


def pop():
    conn = redis.Redis(connection_pool=pool)
    data = conn.brpop("cyber_os_queue", timeout=10)
    if not data:
        return
    return data[1].decode("utf-8")


def fetch_one(sql, params):
    conn = db_pool.connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        return result
    finally:
        conn.close()


def db_queue_init():  # 先查询一下redis队列中没有 然而mysql数据库中未完成的订单
    # 1.先去mysql里面获取所有未完成的订单id
    db_list = fetch_all("select order_id from `order` where status=1", [])
    unfinished_order_id_list = {item["order_id"] for item in db_list}

    # 2.再去redis里面获取所有的id
    conn = redis.Redis(connection_pool=pool)
    total_count = conn.llen("cyber_os_queue")
    cache_list = conn.lrange(name="cyber_os_queue", start=0, end=total_count)
    cache_list_init = {int(item.decode("utf-8")) for item in cache_list}

    # 3.对比redis和mysql
    need_push = unfinished_order_id_list - cache_list_init

    # 4.重新放入redis队列中
    if need_push:
        conn.lpush("cyber_os_queue", *need_push)


def get_order_object(order_id):
    res = fetch_one("select * from `order` where order_id=%s", [order_id])
    return res


def db_update(sql, params):
    conn = db_pool.connection()
    try:
        with conn.cursor(cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
        conn.commit()
    finally:
        conn.close()
        return cursor.lastrowid


def update_order(order_id, status):
    db_update("update `order` set status=%s where order_id=%s", [status, order_id])


def run():
    db_queue_init()
    while 1:
        order_id = pop()
        print(order_id)
        if not order_id:
            continue

        # 查看订单是否存在(可能下单之后又删除订单了)
        order_dict = get_order_object(order_id)
        if not order_dict:
            continue

        # 更新订单状态
        update_order(order_id, 2)

        # 执行订单
        time.sleep(5)

        # 执行完成 更新订单状态
        update_order(order_id, 3)


if __name__ == "__main__":
    run()
