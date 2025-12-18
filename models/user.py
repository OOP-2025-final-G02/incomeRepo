
from peewee import Model, CharField, IntegerField, DateTimeField
from datetime import datetime
from .db import db

class User(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.now)
    workplace = CharField()
    income = IntegerField()

    class Meta:
        database = db
