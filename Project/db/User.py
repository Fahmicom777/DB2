import redis
import json
import random
import db.Login

userTypes = ["Listener", "Artist", "Admin", "Undefined"]

class User:
    def __init__(self):
        self.userType = userTypes[3]

    def saveUser(self, redis_client, user):
        if (db.Login.registrationCheck(redis_client, user["name"], self.userType)):
            print("Name already taken")
            return False
        key = random.randint(0, 1000)
        redis_client.hset(self.userType, key, json.dumps(user))
        return key

    def findUser(self, redis_client, key):
        if key is None or key is False: 
            print("Invalid Key " + self.userType)
            return False
        value = redis_client.hget(self.userType, key)
        if value is None:
            return False
        return json.loads(value)

    def login(self, redis_client, rName, rPassword):
        if db.Login.login(redis_client, rName, rPassword, self.userType):
            return "Login as " + self.userType + " successful!"
        else:
            return "Login as " + self.userType + " Faild!"

class Listener(User):
    def __init__(self):
        super().__init__()
        self.userType = userTypes[0]

    def setPayment(index):
        db.Payment.setPayment(index)

class Artist(User):
    def __init__(self):
        super().__init__()
        self.userType = userTypes[1]

    def uploadSong(self, song):
        pass

class Admin(User):
    def __init__(self):
        super().__init__()
        self.userType = userTypes[2]

    def findUserByName(self, redis_client, name):
        if not isinstance(name, str):
            print("Invalid Name entered")
            return False
        
        userTypes = ["Listener", "Artist"]
        for findType in userTypes:
            keys = redis_client.hgetall(findType).keys()
            for key in keys:
                value = redis_client.hget(findType, key)
                if value != None:
                    value = json.loads(value)
                    if name == value["name"]:
                        return {"key": key, "userType": findType, "value": value}
        return None
    
    def deleteUser(self, redis_client: redis.Redis, key: bytes, userType: str):
        if userType != userTypes[0] or userType != userTypes[1]:
            print("User of given user type can't be deleted by others")
        if redis_client.hdel(userType, key):
            print("User successful deleted")
        else:
            print("No user with given key and type was found")