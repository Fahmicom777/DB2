import redis
import json
import random

def setRating(redis_client:redis.Redis, lKey: int, sKey: int, rating: int):
    rKey = random.randint(1, 1000)
    keys = redis_client.hgetall("Rating").keys()
    
    done = False
    while not done:
        done = True
        for key in keys:
            if rKey == key:
                done = False
                rKey = random.randint(1, 1000)
                break
    redis_client.hset("Rating", rKey, json.dumps({"Listener": lKey, "Song": sKey, "Rating": rating}))

def getRating(redis_client:redis.Redis, rKey: int):
    return json.loads(redis_client.hget("Rating", rKey))

def getAllRatingKeysFrom(redis_client: redis.Redis, key: int, type: int):
    rKeys = []
    allKeys = redis_client.hgetall("Rating").keys()
    for rKey in allKeys:
        rating = getRating(redis_client, rKey)
        if rating[type] == key:
            rKeys.append(rKey)
    return rKeys

def getAllRatingsFromKey(redis_client: redis.Redis, key: int, type: str):
    ratings = []
    rKeys = getAllRatingKeysFrom(redis_client, key, type)
    for rKey in rKeys:
        ratings.append(getRating(redis_client, rKey))
    return ratings

def deleteAllRatingsFromListener(redis_client: redis.Redis, key: int):
    rKeys = getAllRatingKeysFrom(redis_client, key, "Listener")
    for rKey in rKeys:
        redis_client.hdel("Rating", rKey)
