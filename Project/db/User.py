import redis
import json
import random
import db.Login

class User:
    def __init__(self, userType):
        self.userType = userType

    def save_user(self, redis_client, user):
        
        if (db.Login.registrationCheck(redis_client, user["name"], self.userType)):
            return False
        key = random.randint(0, 1000)
        redis_client.hset(self.userType, key, json.dumps(user))
        return key

    def find_user(self, redis_client, key):
        value = redis_client.hget(self.userType, key)
        if value is None:
            return False
        return json.loads(value)

    def login(self, redis_client, rName, rPassword):
        return db.Login.login(redis_client, rName, rPassword, self.userType)