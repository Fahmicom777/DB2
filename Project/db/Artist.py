import redis
import json
import random
from User import User
import Login, Song

#TO-DO: Song reference to all songs of that one artist

class Artist(User):
    def __init__(self):
        super().__init__()
        self.userType = "Artist"

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