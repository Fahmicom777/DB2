import redis
import json
from User import User
import Payment, Rating

class Listener(User):
    def __init__(self):
        super().__init__()
        self.userType = "Listener"

    def setPayment(self, redis_client: redis.Redis, pOptions: dict[any], lKey: int):
        payment = Payment.getPaymentKey(redis_client, pOptions)
        listener = self.findUser(redis_client, lKey)
        listener["payment"] = payment
        print(listener)
        redis_client.hset(self.userType, lKey, json.dumps(listener))
    
    def setRating(self, redis_client:redis.Redis, lKey: int, sKey: int, rating: int):
        if self.isKey(lKey) and self.isKey(sKey):
            if rating >= 0 and rating <= 10:
                Rating.setRating(redis_client, lKey, sKey, rating)
            else:
                print("Rating must be between 0 and 10 (including 0 and 10)")
    
    def getRating(self, redis_client:redis.Redis, lKey: int, sKey: int):
        if self.isKey(lKey) or self.isKey(sKey):
            return Rating.getRating(redis_client, lKey, sKey)

    def getHistory(self, redis_client:redis.Redis, lKey: int):
        if self.isKey(lKey):
            return Rating.getHistory(redis_client, lKey)