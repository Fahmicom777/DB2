import redis
import json

def login(redis_client, rName, rPassword, userType):
    keys = redis_client.hgetall("Listener").keys()
    for key in keys:
        value = json.loads(redis_client.hget(userType, key))
        if rPassword == value["password"] and rName == value["name"]:
            return True
    return False

def registrationCheck(redis_client, rName, userType):
    keys = redis_client.hgetall("Listener").keys()
    for key in keys:
        value = json.loads(redis_client.hget(userType, key))
        if rName == value["name"]:
            return True
    return False