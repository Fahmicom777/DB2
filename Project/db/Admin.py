import redis
import json
from User import User
import Song, Rating


class Admin(User):
    def __init__(self):
        super().__init__()
        self.userType = "Admin"

    def authArtist(self, redis_client: redis.Redis, artistKey, adminKey):
        artist = json.loads(redis_client.hget("Artist", artistKey))
        if (artist["Auth"] is None):
            artist["Auth"] = int(adminKey)
            print(artist)
            redis_client.hset("Artist", artistKey, json.dumps(artist))
        else:
            print("Artist already authenticated")

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
    
    def deleteUser(self, redis_client: redis.Redis, key: int, userType: str):
        if userType != self.userType and userType != self.userType:
            print("User of given user type can't be deleted by others")
        elif self.isKey(key):
            if userType == self.userTypes[1]:
                Song.deletAllSongsFromArtist(redis_client, key)
            if userType == self.userTypes[0]:
                Rating.deleteAllRatingsFromListener(redis_client, key)
            if redis_client.hdel(userType, key):
                print("User successful deleted")
            else:
                print("No user with given key and type was found")