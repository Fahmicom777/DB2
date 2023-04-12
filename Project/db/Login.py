import redis
import json
def login(redis_client, rName, rPassword, userType):
    keys = redis_client.hgetall(userType).keys()
    for key in keys:
        value = json.loads(redis_client.hget(userType, key))
        if rPassword == value["password"] and rName == value["name"]:
            return True
    return False

def registrationCheck(redis_client, rName, userType):
    #get all keys from userType
    keys = redis_client.hgetall(userType).keys()
    for key in keys:
        print("bub")
        #check if entered name is used by one of the useres
        value = redis_client.hget(userType, key)
        if value != None:
            if rName == json.loads(value)["name"]:
                return True
    return False