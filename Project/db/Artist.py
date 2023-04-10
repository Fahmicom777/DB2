import redis
import json
import db.Login, db.User, db.Song, db.Admin

class Artist(db.User):
    def __init__(self, userType):
        super().__init__(userType)

    def uploadSong(self, song):
        pass