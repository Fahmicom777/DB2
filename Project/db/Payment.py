import redis
import json

payments = {0: "Paypal", 1:"Kredit", 2:"Option3"}
def getOptions():
    for i in payments:
        print(i)

def getPayment(index):
    return payments[index]

def setPayment(nPayment):
    match nPayment:
        case "Paypal":
            return 0
        case "Kradit":
            return 1
        case "Option3":
            return 2