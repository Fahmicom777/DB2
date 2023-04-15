import redis
import json
import Rating
import random
import KeyGenerator
classType = "Song"

def isKey(key):
    if key is None or key is False: 
        print("Invalid Key")
        return False

def uploadSong(redis_client:redis.Redis, song: dict[any], artistUploads: list[int]):
    for artistSong in artistUploads:
        if artistSong is None:
            break
        if json.loads(redis_client.hget(classType, artistSong)) == song:
            print("Song with same informations already uploaded")
            return artistSong
    keys = redis_client.hgetall("Rating").keys()
    sKey = KeyGenerator.generateKey([0, 1000], keys)
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
    return artistSongs

def deletAllSongsFromArtist(redis_client:redis.Redis, artistKey: int):
    artistSongs = getAllSongsFromArtist(redis_client, artistKey)
    print("Songs to delete: " + str(len(artistSongs)))
    for artistsong in artistSongs:
        redis_client.hdel("Song", artistsong["Key"])
    print("Songs deleted")