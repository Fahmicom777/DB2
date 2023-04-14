import redis
import json
import random
import Login, Song, Payment, Rating

userTypes = ["Listener", "Artist", "Admin", "Undefined"]


    
class User:
    def __init__(self):
        #self.redis_client = redis_client
        self.userType = userTypes[3]

    def isKey(self, key):
        if key is None or key is False: 
            print("Invalid Key")
            return False
        return True

    def saveUser(self, redis_client, user):
        #Check if name within the userType is already taken
        if (Login.registrationCheck(redis_client, user["name"], self.userType)):
            print("Name already taken")
            return False
        #generate Key and save user
        #TO-DO: Check if key already exists
        key = random.randint(0, 1000)
        redis_client.hset(self.userType, key, json.dumps(user))
        return key

    def findUser(self, redis_client, key):
        #Check if Key is functionable 
        if key is None or key is False: 
            print("Invalid Key")
            return False
        #get addressed value of the given key
        value = redis_client.hget(self.userType, key)
        if value is None:
            print("Key value is empty")
            return False
        return json.loads(value)

    def login(self, redis_client, rName, rPassword):
        if Login.login(redis_client, rName, rPassword, self.userType):
            return "Login as " + self.userType + " successful!"
        else:
            return "Login as " + self.userType + " Faild!"

class Listener(User):
    def __init__(self):
        super().__init__()
        self.userType = userTypes[0]

    def setPayment(self, redis_client: redis.Redis, pOptions: dict[any], lKey: int):
        payment = Payment.getPaymentKey(redis_client, pOptions)
        listener = self.findUser(redis_client, lKey)
        listener["payment"] = payment
        print(listener)
        redis_client.hset(self.userType, lKey, json.dumps(listener))
    
    def setRating(self, redis_client:redis.Redis, lKey: int, sKey: int, rating: int):
        if self.isKey(lKey) and self.isKey(sKey):
            if rating >= 0 and rating <= 10:
                Rating.setRating(redis_client, lKey, sKey, rating)
            else:
                print("Rating must be between 0 and 10 (including 0 and 10)")
    
    def getRating(self, redis_client:redis.Redis, lKey: int, sKey: int):
        if self.isKey(lKey) or self.isKey(sKey):
            return Rating.getRating(redis_client, lKey, sKey)

    def getHistory(self, redis_client:redis.Redis, lKey: int):
        if self.isKey(lKey):
            return Rating.getHistory(redis_client, lKey)

class Artist(User):
    def __init__(self):
        super().__init__()
        self.userType = userTypes[1]

    def saveUser(self, redis_client, user):
        user["Auth"] = None
        if (Login.registrationCheck(redis_client, user["name"], self.userType)):
            print("Name already taken")
            return False
        key = random.randint(0, 1000)
        redis_client.hset(self.userType, key, json.dumps(user))
        return key
        
    def uploadSong(self, redis_client: redis.Redis, song: dict, artistKey: int, addArtists: list[any]):
        #Check if key is not empty
        if not self.isKey(artistKey):
            print("No Artist was given")
            return None
        #Check if Artist has its Auth filled out
        auth = json.loads(redis_client.hget("Artist", artistKey))["Auth"]
        if auth == None:
            print("Artist has not been authenticated")
            return None
        #Enter Artist and additional Artists to song
        song["Artist"] = artistKey
        if addArtists != None:
            #Additional Aritsts can't contain lead Artist
            for addArtist in addArtists:
                if addArtist is artistKey:
                    print("Creater of the Song can not be entered as 'additional Artist'")
                    continue
                #Check if additional Artist can be fount in Artist Database
                artist = self.findUser(redis_client, addArtist)
                if artist:
                    #add additional Artist to song
                    
                    if not song.keys().__contains__("addArtists"):
                        song["addArtists"] = [addArtist]
                    else:
                        double = False
                        for savedAddArtist in song["addArtists"]:
                            if savedAddArtist == addArtist:
                                double = True
                                print("Entered additional artist Nr." + str(song["addArtists"].index(savedAddArtist)) + " is already saved in this Song")
                                break
                        if not double:
                            song["addArtists"].append(addArtist)
                else:
                    print("Additional Artist Nr." + str(addArtists.index(addArtist)) + " not found")
        #Upload Song
        return Song.uploadSong(redis_client, song, artistKey)
    
    def authArtsit(self, redis_client: redis.Redis, adminKey: int):
        if self.authentification == None:
            adminKeys = redis_client.hgetall("Admin")
            for key in adminKeys:
                if adminKey == key:
                    self.authentification = adminKey
                    break

class Admin(User):
    def __init__(self):
        super().__init__()
        self.userType = userTypes[2]

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
        if userType != userTypes[0] and userType != userTypes[1]:
            print("User of given user type can't be deleted by others")
        elif self.isKey(key):
            if userType == userTypes[1]:
                Song.deletAllSongsFromArtist(redis_client, key)
            if userType == userTypes[0]:
                Rating.deleteAllRatingsFromListener(redis_client, key)
            if redis_client.hdel(userType, key):
                print("User successful deleted")
            else:
                print("No user with given key and type was found")