import redis
import json
import unittest
import Payment, Rating
from Listener import Listener
from Artist import Artist
from Admin import Admin
# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
listener = Listener()
artist = Artist()
admin = Admin()

#listener = Listener()
#artist = Artist()
#admin = Admin()

cTables = ["Payment", "Rating", "Song", "Listener", "Artist", "Admin"]


bob = {'name': "bob", 'born': 1986, 'password': "DE"}
alice = {'name': "alice", 'born': 1995, 'password': "DE1"}
bob1 = {'name': "nicht Bob", 'born': 1986, 'password': "DE"}
alice1 = {'name': "nicht Alice", 'born': 1995, 'password': "DE1"}
bob2 = {'name': "Artist Bob", 'born': 1986, 'password': "DE"}
ingit = {'name': "ingit", 'born': 19951, 'password': "DE11"}

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
        Payment.setPayment(redis_client, payment)
        Payment.setPayment(redis_client, payment1)
        
        cls.lKey = listener.saveUser(redis_client, alice)
        cls.lKey2 = listener.saveUser(redis_client, alice1)
        cls.arKey = artist.saveUser(redis_client, bob)
        cls.arKey2 = artist.saveUser(redis_client, bob1)
        cls.arKey3 = artist.saveUser(redis_client, bob2)
        cls.adKey = admin.saveUser(redis_client, ingit)
        
        cls.sKey1 = None
        cls.sKey2 = None
        cls.sKey3 = None
        for _key in cTables:
            for i in redis_client.hgetall(_key).keys():
                print(_key, redis_client.hget(_key, i))

        print("Lets go")

    def setUp(self):
        print("-----------")


    #Artist
    def test_ArtistUploadsSong(self):
        #Check for Authentification
        self.sKey = artist.uploadSong(redis_client, song1, self.arKey, None)
        self.assertIsNone(self.sKey)
        admin.authArtist(redis_client, self.arKey, self.adKey)
        #Upload song with without additional artists
        self.sKey = artist.uploadSong(redis_client, song1, self.arKey, None)
        self.assertIsNotNone(self.sKey)
        #Upload Song with one additional artist
        self.sKey2 = artist.uploadSong(redis_client, song2, self.arKey, [self.arKey2])
        self.assertIsNotNone(self.sKey2)
        #Upload Song with multipule artists
        self.sKey3 = artist.uploadSong(redis_client, song2, self.arKey, [self.arKey2, self.arKey3])
        self.assertIsNotNone(self.sKey3)

    #Listener
    def test_ListenerSetPayment(self):
        listener.setPayment(redis_client, payment, self.lKey)
        lPayment = json.loads(redis_client.hget("Listener", self.lKey))["payment"]
        sPayment = Payment.getPaymentKey(redis_client, payment)
        print("Listeners payment option key: " + str(lPayment), "| Saved payment option key: " + str(sPayment))
        self.assertEqual(lPayment, sPayment)

    #AYO
    def test_ListenerGivesRating(self):
        #Upload song with without additional artists
        admin.authArtist(redis_client, self.arKey, self.adKey)
        self.sKey = artist.uploadSong(redis_client, song1, self.arKey, None)
        #Rating that song
        listener.setRating(redis_client, self.lKey, self.sKey, 7)
        #Check if Rating of this listener is saved
        sRating = Rating.getAllRatingsFromKey(redis_client, self.lKey, "Listener")[0]
        cRating = {"Listener": self.lKey, "Song": self.sKey, "Rating": 7}
        
        self.assertEqual(str(sRating), str(cRating))

    def ListenerChangesRating(self):
        print("test")
        self.assertTrue(True)

    def ListenerChecksRating(self):
        print("test")
        self.assertTrue(True)

    #Admin
    def test_XAdminDeletesUser(self):
        print("aödfioghwüofghaöelfjkghöaeigjk")
        admin.deleteUser(redis_client, self.lKey, "Listener")
        self.assertFalse(redis_client.hget("Listener", self.lKey))

    @classmethod
    def tearDownClass(cls):
        for _key in cTables:
            for i in redis_client.hgetall(_key).keys():
                print(_key, json.loads(redis_client.hget(_key, i)))
                redis_client.hdel(_key, i)
        print("------bye-bye------")