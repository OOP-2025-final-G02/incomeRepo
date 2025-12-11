from peewee import Model, CharField, IntegerField
from .db import db

class User(Model):
    name = CharField() 
    created_at = IntegerField()
    workplace = CharField()
    income = IntegerField()


    class Meta:
        database = db