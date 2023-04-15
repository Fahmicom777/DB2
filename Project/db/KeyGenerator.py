import random

def generateKey(keyRange: list[int], existingKeys):
    rKey = random.randint(keyRange[0], keyRange[1])
    
    done = False
    while not done:
        done = True
        for key in existingKeys:
            if rKey == key:
                done = False
                rKey = random.randint(1, 1000)
                break
    print("generated key: " + str(rKey))
    return rKey