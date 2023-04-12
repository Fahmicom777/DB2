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

def getAllRatingsFromKey(redis_client: redis.Redis, key: int, type: int):
    ratings = []
    rKeys = redis_client.hgetall("Rating").keys()
    for rKey in rKeys:
        rating = getRating(redis_client, rKey)
        if rating[type] == key:
            ratings.append(rating)
    print(ratings)