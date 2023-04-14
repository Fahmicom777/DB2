import redis
import json
import db.User, db.Payment

# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
listener = db.User.Listener()
artist = db.User.Artist()
admin = db.User.Admin()

bob = {'name': "bob", 'password': "DE"}
alice = {'name': "alice", 'password': "DE1"}
bob1 = {'name': "nicht Bob", 'password': "DE"}
alice1 = {'name': "nicht Alice", 'password': "DE1"}
ingit = {'name': "ingit", 'password': "DE11"}

testUser = {'name': "Artist Bob", 'password': "DE"}

song1 = {"titel": "Song1", "Artist": None}
song2 = {"titel": "Song2", "Artist": None}

payment = {"name": "Paypal", "subModel": "VIP"}
payment1 = {"name": "Creditcard", "subModel": "Basic"}

#print(db.Payment.setPayment(redis_client, payment))
#print(db.Payment.setPayment(redis_client, payment1))
redis_client.hdel("Payment", 2)
redis_client.hdel("Payment", 3)
key = redis_client.hgetall("Rating").keys()
for i in redis_client.hgetall("Rating").keys():
    print(i)
    redis_client.hdel("Rating", i)

for i in redis_client.hgetall("Song").keys():
    print(i)
    redis_client.hdel("Song", i)

#testKey = artist.saveUser(redis_client, testUser)
#testKey = b'428'
#artist.uploadSong(redis_client, song1, testKey)

#admin.deleteUser(redis_client, testKey, "Artist")

print("----------Artist---------")
keyArtist = artist.saveUser(redis_client, bob)
print(keyArtist)
sKey = None
sKey1 = None
if keyArtist:
    keys = redis_client.hgetall("Artist").keys()
    for lkey in keys:
        print(lkey)
    value = artist.findUser(redis_client, keyArtist)
    print(value)
    print(artist.login(redis_client, value["name"], value["password"]))
    print("---------Authentification")
    artist.uploadSong(redis_client, song1, keyArtist, None)
    admin.authArtist(redis_client, keyArtist, b'895')
    print("---------Song 1")
    sKey1 = artist.uploadSong(redis_client, song1, keyArtist, None)
    print(sKey)
    print("---------Song 2")
    #test = artist.saveUser(redis_client, testUser)
    #admin.authArtist(redis_client, keyArtist, b'895')
    sKey = artist.uploadSong(redis_client, song2, keyArtist, [450, 771, 451, keyArtist])
    print(sKey)
    print(redis_client.hgetall("Song").items())
print("----------Listener---------")
lKey = listener.saveUser(redis_client, alice)
if lKey:
    keys = redis_client.hgetall("Listener").keys()
    for key in keys:
        print(key)
    
    listener.setPayment(redis_client, payment, lKey)
    value = listener.findUser(redis_client, lKey)
    print(listener.login(redis_client, value["name"], value["password"]))
    listener.setRating(redis_client, lKey, sKey, 7)
    listener.setRating(redis_client, lKey, sKey1, 5)
    import db.Rating
    db.Rating.getAllRatingsFromKey(redis_client, lKey, "Listener")
    db.Rating.getAllRatingsFromKey(redis_client, sKey, "Song")
print("----------Admin---------")

keys = redis_client.hgetall("Admin").keys()
for key in keys:
    print(key)

#keyAdmin = admin.save_user(redis_client, ingit)
keyAdmin = b'895'
#print (keyAdmin)
value = admin.findUser(redis_client, keyAdmin)
print(value)
print(admin.login(redis_client, value["name"], value["password"]))
for name in "alice", "bob":
    deleteListener = admin.findUserByName(redis_client, name)
    if deleteListener != None:
        print(deleteListener["key"], deleteListener["userType"], deleteListener["value"])
        admin.deleteUser(redis_client, deleteListener.get("key"), deleteListener.get("userType"))

## Hab zuerst versucht etwas mit zadd zu reisen. Ich hab net geblickt, wie man individuelle einträge einsehen kann.
## jetzt switche ich zu hset (redis hashes). Das wurde ja in der Vorlesung auch unterrichtet

#redis_client.zadd('vehicles', {'car' : 0})
#redis_client.zadd('vehicles', {'bike' : 0})
#vehicles = redis_client.zrange('vehicles', 0, -1)
#length = len(vehicles) - 1
#print(vehicles)
#redis_client.zremrangebyrank('vehicles', 0, length)
#print(redis_client.zrange('vehicles', 0, -1))
#print(redis_client.get('vehicles: 1'))

#print(user.find_user(redis_client, 8))
#print(user.find_user(redis_client, 12))
#print(user.r.zrange('Listener', 0, -1))

#save_user(bob)

#print(find_user(8))
#find_user(8)







# Set a key-value pair
#redis_client.set("hello", "world")

# Get the value of the key
#value = redis_client.get("hello")