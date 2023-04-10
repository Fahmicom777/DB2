import redis
import json
import db.Listener

# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
user = db.Listener


bob = {'id': 8, 'name': "bob", 'born': 1986, 'password': "DE", "payment": None}
alice = {'id': 12, 'name': "alice", 'born': 1995, 'password': "DE1", "payment": None}
alice1 = {'id': 121, 'name': "alice", 'born': 19951, 'password': "DE11", "payment": None}

song1 = {"titel": "Song1", "Artist": 123,}

key1 = user.save_user(redis_client, alice1)
print(key1)
#redis_client.hdel("Listener", b"644")
key = 476
value = user.find_user(redis_client, key)
if value == None:
    print(value)
else:
    print(value)

keys = redis_client.hgetall("Listener").keys()
for key in keys:
    print(key)

print(user.login(redis_client, "alice", "DE1"))

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