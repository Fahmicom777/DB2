import redis
import json
import random
import Login, Song
from user.User import User


class Artist(User):
    def __init__(self, redis_client: redis.Redis):
        super().__init__(redis_client)
        self.userType = "Artist"

    def saveUser(self, user):
        user["Auth"] = None
        if (Login.registrationCheck(self.redis_client, user["name"], self.userType)):
            print("Name already taken")
            return False
        key = random.randint(0, 1000)
        self.redis_client.hset(self.userType, key, json.dumps(user))
        return key
    
    def uploadSong(self, song: dict, artistKey: int, fArtists: list[any]):
        #Check if key is not empty
        if not self.isKey(artistKey):
            print("No Artist was given")
            return None
        #Check if Artist has its Auth filled out
        auth = json.loads(self.redis_client.hget("Artist", artistKey))["Auth"]
        if auth == None:
            print("Artist has not been authenticated")
            return None
        #Enter Artist and additional Artists to song
        song["Artist"] = artistKey
        if fArtists != None:
            #Additional Aritsts can't contain lead Artist
            for fArtist in fArtists:
                if fArtist is artistKey:
                    print("Creater of the Song can not be entered as 'featuring Artist'")
                    continue
                #Check if additional Artist can be fount in Artist Database
                artist = self.findUser(fArtist)
                if artist:
                    #add additional Artist to song
                    
                    if not song.keys().__contains__("fArtists"):
                        song["fArtists"] = [fArtist]
                    else:
                        double = False
                        for savedfArtist in song["fArtists"]:
                            if savedfArtist == fArtist:
                                double = True
                                print("Entered additional artist Nr." + str(song["fArtists"].index(savedfArtist)) + " is already saved in this Song")
                                break
                        if not double:
                            song["fArtists"].append(fArtist)
                else:
                    print("Featuring Artist Nr." + str(fArtists.index(fArtist)) + " not found")
        #Upload Song
        uploads = self.getUploadedSongs(artistKey)
        sKey = Song.uploadSong(self.redis_client, song, uploads)
        if sKey is not None:
            #Save reference of song to artist
            artist = self.findUser(artistKey)
            if "Uploads" in artist:
                artist["Uploads"].append(sKey)
            else:
                artist["Uploads"] = [sKey]
            self.redis_client.hset("Artist", artistKey, json.dumps(artist))
            return sKey
        else:
            return None
    
    def authArtsit(self, adminKey: int):
        if self.authentification == None:
            adminKeys = self.redis_client.hgetall("Admin")
            for key in adminKeys:
                if adminKey == key:
                    self.authentification = adminKey
                    break
    
    def getUploadedSongs(self, artistKey: int):
        artist = self.findUser(artistKey)
        if "Uploads" in artist:
            return artist["Uploads"]
        else:
            return []