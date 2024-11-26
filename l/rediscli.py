import redis

def connect_to_redis():
    try:
        client = redis.StrictRedis(
            host='124.220.6.43',
            port=6379,
            password='root123456',
            decode_responses=True
        )
        # Test the connection
        client.ping()
        return client
    except redis.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        return None


def get_redis_client():
    return connect_to_redis()
