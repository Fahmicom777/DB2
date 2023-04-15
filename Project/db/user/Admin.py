import redis
import json
import Song, Rating
from user.User import User

userTypes = ["Listener", "Artist"]

class Admin(User):
    def __init__(self, redis_client: redis.Redis):
        super().__init__(redis_client)
        self.userType = "Admin"

    def authArtist(self, artistKey, adminKey):
        artist = json.loads(self.redis_client.hget(userTypes[1], artistKey))
        if (artist["Auth"] is None):
            artist["Auth"] = int(adminKey)
            print(artist)
            self.redis_client.hset(userTypes[1], artistKey, json.dumps(artist))
        else:
            print("Artist already authenticated")

    def findUserByName(self, name):
        if not isinstance(name, str):
            print("Invalid Name entered")
            return False
        
        for findType in userTypes:
            keys = self.redis_client.hgetall(findType).keys()
            for key in keys:
                value = self.redis_client.hget(findType, key)
                if value != None:
                    value = json.loads(value)
                    if name == value["name"]:
                        return {"key": key, "userType": findType, "value": value}
        return None
    
    def deleteUser(self, key: int, userType: str):
        if userType != userTypes[0] and userType != userTypes[1]:
            print("User of given user type can't be deleted by others")
        elif self.isKey(key):
            if userType == userTypes[1]:
                Song.deletAllSongsFromArtist(self.redis_client, key)
            if userType == userTypes[0]:
                Rating.deleteAllRatingsFromListener(self.redis_client, key)
            if self.redis_client.hdel(userType, key):
                print("User successful deleted")
            else:
                print("No user with given key and type was found")