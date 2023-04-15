import redis
import json
import unittest
import Payment, Rating
from user.Listener import Listener
from user.Artist import Artist
from user.Admin import Admin
# Connect to Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
listener = Listener(redis_client)
artist = Artist(redis_client)
admin = Admin(redis_client)

cTables = ["Payment", "Rating", "Song", "Listener", "Artist", "Admin"]

bob = {'name': "bob", 'password': "DE"}
alice = {'name': "alice", 'password': "DE1"}
bob1 = {'name': "nicht Bob", 'password': "DE"}
alice1 = {'name': "nicht Alice", 'password': "DE1"}
bob2 = {'name': "Artist Bob", 'password': "DE"}
ingit = {'name': "ingit", 'password': "DE11"}

song0 = {"titel": "Zero", "artist": None}
song1 = {"titel": "Song1", "artist": None}
song2 = {"titel": "Song2", "artist": None}


payment = {"name": "Paypal", "subModel": "VIP"}
payment1 = {"name": "Paypal", "subModel": "Basic"}



if __name__ == '__main__':
    unittest.main(verbosity=1)

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Payment.setPayment(redis_client, payment)
        Payment.setPayment(redis_client, payment1)
        
        cls.lKey = listener.saveUser(alice)
        cls.lKey2 = listener.saveUser(alice1)
        cls.arKey = artist.saveUser(bob)
        cls.arKey2 = artist.saveUser(bob1)
        cls.arKey3 = artist.saveUser(bob2)
        cls.adKey = admin.saveUser(ingit)
        
        cls.sKey1 = None
        cls.sKey2 = None
        cls.sKey3 = None
        for _key in cTables:
            for i in redis_client.hgetall(_key).keys():
                print(_key, redis_client.hget(_key, i))

        print("Initiating Tests")
        print("-----------")

    def setUp(self):
        print("----------")
        print("-----------")

    #Artist
    def test_1ArtistUploadsSong(self):
        #Check for Authentification
        self.sKey = artist.uploadSong(song1, self.arKey, None)
        self.assertIsNone(self.sKey)
        admin.authArtist(self.arKey, self.adKey)
        #Upload song with without additional artists
        self.sKey = artist.uploadSong(song1, self.arKey, None)
        self.assertIsNotNone(self.sKey)
        #Upload Song with the exact same informations
        temp = artist.uploadSong(song1, self.arKey, None)
        self.assertEqual(temp, self.sKey)
        #Upload Song with one additional artist
        self.sKey2 = artist.uploadSong(song2, self.arKey, [self.arKey2])
        self.assertIsNotNone(self.sKey2)
        #Upload Song with multipule artists
        self.sKey3 = artist.uploadSong(song2, self.arKey, [self.arKey2, self.arKey3])
        self.assertIsNotNone(self.sKey3)
        print("-----------")

    #Listener
    def test_2ListenerSetPayment(self):
        listener.setPayment(payment, self.lKey)
        lPayment = json.loads(redis_client.hget("Listener", self.lKey))["payment"]
        sPayment = Payment.getPaymentKey(redis_client, payment)
        print("Listeners payment option key: " + str(lPayment), "| Saved payment option key: " + str(sPayment))
        self.assertEqual(lPayment, sPayment)
        print("-----------")

    def test_3ListenerGivesRating(self):
        #Upload song with without additional artists
        admin.authArtist(self.arKey, self.adKey)
        
        self.sKey = artist.uploadSong(song1, self.arKey, None)
        
        #Rating that song
        listener.setRating(self.lKey, self.sKey, 7)
        #Check if Rating of this listener is saved
        sRating = Rating.getAllRatingsFromKey(redis_client, self.lKey, "Listener")[0]
        cRating = {"Listener": self.lKey, "Song": self.sKey, "Rating": 7}
        
        self.assertEqual(str(sRating), str(cRating))
        print("-----------")


    def test_4ListenerChangesRating(self):
        #Create Rating
        admin.authArtist(self.arKey, self.adKey)
        self.sKey = artist.uploadSong(song0, self.arKey, None)
        listener.setRating(self.lKey, self.sKey, 7)

        #Check if song0 is created
        sRatings = Rating.getAllRatingsFromKey(redis_client, self.lKey, "Listener")
        cRating = {"Listener": self.lKey, "Song": self.sKey, "Rating": 7}
        self.assertTrue(cRating in sRatings)
        
        #Change rating
        listener.setRating(self.lKey, self.sKey, 5)
        
        #Check if Rating of song0 from listener is changed
        newRatings = Rating.getAllRatingsFromKey(redis_client, self.lKey, "Listener")
        newRating = {"Listener": self.lKey, "Song": self.sKey, "Rating": 5}
        #Check if rating was changed
        self.assertTrue(newRating in newRatings) #Rating is 5 now
        self.assertFalse(cRating in newRatings) #Old Value is not saved
        print("-----------")


    def test_5ListenerChecksRating(self):
        #upload Songs and rate them
        admin.authArtist(self.arKey, self.adKey)
        self.sKey = artist.uploadSong(song0, self.arKey, None)
        listener.setRating(self.lKey, self.sKey, 7)
        self.sKey1 = artist.uploadSong(song1, self.arKey, None)
        listener.setRating(self.lKey, self.sKey, 7)

        #These should be the created ratings
        rating = {"Listener": self.lKey, "Song": self.sKey, "Rating": 7}
        rating2 = {"Listener": self.lKey, "Song": self.sKey1, "Rating": 7}
        ratings = [rating, rating2]

        #Get one Rating from User
        sRating = listener.getRating(self.lKey, self.sKey)
        self.assertEqual(rating, ratings[0])

        #Get all Ratings from User
        sRating = listener.getHistory(self.lKey)
        for rating in ratings:
            self.assertTrue(rating in sRating)
        print("-----------")

    #Admin
    def test_6AdminDeletesUser(self):
        admin.deleteUser(self.lKey, "Listener")
        self.assertFalse(redis_client.hget("Listener", self.lKey))
        print("-----------")

    @classmethod
    def tearDownClass(cls):
        for _key in cTables:
            for i in redis_client.hgetall(_key).keys():
                print(_key, i, json.loads(redis_client.hget(_key, i)))
                redis_client.hdel(_key, i)
        print("------bye-bye------")