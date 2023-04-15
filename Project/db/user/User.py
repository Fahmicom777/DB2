import redis
import json
import Login, KeyGenerator
    
class User:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.userType = "Undefined"

    def isKey(self, key):
        if key is None or key is False: 
            print("Invalid Key")
            return False
        return True

    def saveUser(self, user):
        #Check if name within the userType is already taken
        if (Login.registrationCheck(self.redis_client, user["name"], self.userType)):
            print("Name already taken")
            return False
        #generate Key and save user
        keys = self.redis_client.hgetall(self.userType).keys()
        key = KeyGenerator.generateKey([0, 1000], keys)
        self.redis_client.hset(self.userType, key, json.dumps(user))
        return key

    def findUser(self, key):
        #Check if Key is functionable 
        if key is None or key is False: 
            print("Invalid Key")
            return False
        #get addressed value of the given key
        value = self.redis_client.hget(self.userType, key)
        if value is None:
            print("Key value is empty")
            return False
        return json.loads(value)

    def login(self, rName, rPassword):
        if Login.login(self.redis_client, rName, rPassword, self.userType):
            return "Login as " + self.userType + " successful!"
        else:
            return "Login as " + self.userType + " Faild!"