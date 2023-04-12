import redis
import json
import db.Rating
import random

classType = "Song"

def isKey(key):
    if key is None or key is False: 
        print("Invalid Key")
        return False

def uploadSong(redis_client:redis.Redis, song: dict[any], artistKey: int):
    artistSongs = getAllSongsFromArtist(redis_client, artistKey)
    for artistSong in artistSongs:
        if artistSong == song:
            print("Song with same informations already uploaded")
            return None
    sKey = random.randint(0, 1000)
    redis_client.hset(classType, sKey, json.dumps(song))
    print("Uploaded Song")
    print(song)
    return sKey

def getSong(redis_client:redis.Redis, songKey: int):
    if not isKey:
        return False
    value = redis_client.hget(classType, songKey)
    if value is None:
        return False
    return json.loads(value)

def getAllSongsFromArtist(redis_client:redis.Redis, artistKey: int) -> list:
    artistSongs = []
    keys = redis_client.hgetall("Song").keys()
    for key in keys:
        value = redis_client.hget(classType, key)
        if value != None:
            value = json.loads(value)
            if int(artistKey) == value["Artist"]:
                test = {"Key": key, "Value": value}
                artistSongs.append(test)
    #print(artistSongs)
    return artistSongs

def deletAllSongsFromArtist(redis_client:redis.Redis, artistKey: int):
    artistSongs = getAllSongsFromArtist(redis_client, artistKey)
    print("Songs to delete: " + str(len(artistSongs)))
    for artistsong in artistSongs:
        redis_client.hdel("Song", artistsong["Key"])
    print("Songs deleted")