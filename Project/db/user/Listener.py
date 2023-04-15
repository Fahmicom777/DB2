import redis
import json
import Payment, Rating
from user.User import User

class Listener(User):
    def __init__(self, redis_client: redis.Redis):
        super().__init__(redis_client)
        self.userType = "Listener"

    def setPayment(self, pOptions: dict[any], lKey: int):
        payment = Payment.getPaymentKey(self.redis_client, pOptions)
        listener = self.findUser(lKey)
        listener["payment"] = payment
        print(listener)
        self.redis_client.hset(self.userType, lKey, json.dumps(listener))
    
    def setRating(self, lKey: int, sKey: int, rating: int):
        if self.isKey(lKey) and self.isKey(sKey):
            if rating >= 0 and rating <= 10:
                Rating.setRating(self.redis_client, lKey, sKey, rating)
            else:
                print("Rating must be between 0 and 10 (including 0 and 10)")
    
    def getRating(self, lKey: int, sKey: int):
        if self.isKey(lKey) and self.isKey(sKey):
            ratings = self.getHistory(lKey)
            for rating in ratings:
                if lKey == rating["Listener"] and sKey == rating["Song"]:
                    return rating
            print("No Rating found with given Informations")
        return None

    def getHistory(self, lKey: int):
        if self.isKey(lKey):
            return Rating.getAllRatingsFromKey(self.redis_client, lKey, "Listener")