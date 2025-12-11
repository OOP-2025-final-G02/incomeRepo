from peewee import Model, CharField
from .db import db

class User(Model):
    name = CharField()
    workplace = CharField()

    class Meta:
        database = db
