import redis
import json
import KeyGenerator

def setRating(redis_client:redis.Redis, lKey: int, sKey: int, rating: int):
    keys = redis_client.hgetall("Rating").keys()
    key = KeyGenerator.generateKey([1, 1000], keys)
    nRating = {"Listener": lKey, "Song": sKey, "Rating": rating}

    lRatings = getAllRatingsFromKey(redis_client, lKey, "Listener")
    rKeys = getAllRatingKeysFrom(redis_client, lKey, "Listener")
    for lRating in lRatings:
        print(lRating)
        print(nRating)
        if lRating["Song"] == nRating["Song"]:
            lRating["Rating"] = rating
            key = rKeys[lRatings.index(lRating)]
            break
            
    redis_client.hset("Rating", key, json.dumps(nRating))

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
