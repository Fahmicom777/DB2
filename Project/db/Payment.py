import redis
import json

def setPayment(redis_client: redis.Redis, pOption: dict[str]):
    key = len(redis_client.hgetall("Payment"))
    redis_client.hset("Payment", key, json.dumps(pOption))
    return key

def getPaymentValue(redis_client: redis.Redis, pKey: int):
    return json.loads(redis_client.hget("Payment", pKey))

def getPaymentKey(redis_client: redis.Redis, pOption: dict[any]):
    for i in range(len(redis_client.hgetall("Payment"))):
        option = json.loads(redis_client.hget("Payment", i))
        if option == pOption:
            return i