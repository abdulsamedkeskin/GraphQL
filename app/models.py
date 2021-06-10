import mongoengine as db


class User(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)

    meta = {"collection": "User"}
