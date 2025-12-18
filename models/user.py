from peewee import Model, CharField, IntegerField
from datetime import datetime
from .db import db

class User(Model):
    name = CharField()
    created_at = CharField(default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    workplace = CharField()
    income = IntegerField(default=0)


    class Meta:
        database = db
