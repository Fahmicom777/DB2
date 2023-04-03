import redis
import json

# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)

bob = {'id': 8, 'name': "bob", 'born': 1986, 'country': "DE"}
alice = {'id': 12, 'name': "alice", 'born': 1995, 'country': "DE"}

def save_user(user):
    value = user
    key = user.get("id")
    return redis_client.set(8, json.dumps(bob))

def find_user(id):
    key = id
    value = redis_client.get(key)
    if value is None:
        return False
    return json.loads(value)

save_user(bob)

#import redis
#import json
#
#r = redis.Redis(host="redis")


# def save_user(user):
#  value = json.dumps(user)
#  key = f"users:{user['id']}"
#  return r.set(key, value)
#
#
#def find_user(id):
#  key = f"users:{id}"
#  value = r.get(key)
#  if value is None:
#    return False
#  return json.loads(value)


print(find_user(8))
#find_user(8)







# Set a key-value pair
#redis_client.set("hello", "world")

# Get the value of the key
#value = redis_client.get("hello")