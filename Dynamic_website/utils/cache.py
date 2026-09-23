import redis

pool = redis.ConnectionPool(max_connections=100, decode_responses=True)


def push(value):
    conn = redis.Redis(connection_pool=pool)
    conn.lpush("cyber_os_queue", value)
