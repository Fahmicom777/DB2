import redis
import json
import unittest
import User, Payment

# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
listener = User.Listener()
artist = User.Artist()
admin = User.Admin()

tables = ["Payment", "Rating", "Song", "Listener", "Artsit", "Admin"]

bob = {'name': "bob", 'born': 1986, 'password': "DE"}
alice = {'name': "alice", 'born': 1995, 'password': "DE1"}
bob1 = {'name': "nicht Bob", 'born': 1986, 'password': "DE"}
alice1 = {'name': "nicht Alice", 'born': 1995, 'password': "DE1"}
ingit = {'name': "ingit", 'born': 19951, 'password': "DE11"}

testUser = {'name': "Artist Bob", 'born': 1986, 'password': "DE"}

song1 = {"titel": "Song1", "Artist": None}
song2 = {"titel": "Song2", "Artist": None}

payment = {"name": "Paypal", "subModel": "VIP"}
payment1 = {"name": "Creditcard", "subModel": "Basic"}

if __name__ == '__main__':
    unittest.main(verbosity=1)
    print("boi")

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Lets go")

    def setUp(self):
        #for _key in tables:
        #    for i in redis_client.hgetall(_key).keys():
        #        print(i)
        #        redis_client.hdel("Rating", i)
        print("-----Setup------")

    #Listener
    def test_ListenerSetPayment(self):
        print("test")
        self.assertTrue(True)
        pass

    def test_ListenerGivesRating(self):
        print("test")
        self.assertTrue(True)
        pass

    def test_ListenerChangesRating(self):
        print("test")
        self.assertTrue(True)
        pass

    def test_ListenerChecksRating(self):
        print("test")
        self.assertTrue(True)
        pass

    #Admin
    def test_AdminDeletesUser(self):
        print("test")
        self.assertTrue(True)
        pass

    #Artist
    def test_ArtistUploadsSong(self):
        print("test")
        self.assertTrue(True)
        pass