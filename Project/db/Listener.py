import redis
import json
import db.Payment, db.Rating, db.Login, db.User
import random

class Listener(db.User):
    def __init__(self, userType):
        super().__init__(userType)

    def setPayment(index):
        db.Payment.setPayment(index)