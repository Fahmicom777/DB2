import redis
import json
import db.User

# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
listener = db.User.Listener()
artist = db.User.Artist()
admin = db.User.Admin()

bob = {'id': 8, 'name': "bob", 'born': 1986, 'password': "DE", "payment": None}
alice = {'id': 12, 'name': "alice", 'born': 1995, 'password': "DE1", "payment": None}
bob1 = {'id': 8, 'name': "nicht Bob", 'born': 1986, 'password': "DE", "payment": None}
alice1 = {'id': 12, 'name': "nicht Alice", 'born': 1995, 'password': "DE1", "payment": None}
ingit = {'id': 121, 'name': "ingit", 'born': 19951, 'password': "DE11", "payment": None}

song1 = {"titel": "Song1", "Artist": 123,}

#user.saveUser(redis_client, alice1)
#artist.saveUser(redis_client, bob1)

print("----------")
listenerKey = listener.saveUser(redis_client, alice)
if listenerKey:
    keys = redis_client.hgetall("Listener").keys()
    for lKey in keys:
        print(lKey)

    value = listener.findUser(redis_client, listenerKey)
    print(value)
    print(listener.login(redis_client, value["name"], value["password"]))

print("----------")
keyArtist = artist.saveUser(redis_client, bob)
if keyArtist:
    keys = redis_client.hgetall("Artist").keys()
    for lkey in keys:
        print(lkey)

    value = artist.findUser(redis_client, keyArtist)
    print(value)
    print(artist.login(redis_client, value["name"], value["password"]))

print("----------")

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