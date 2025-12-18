from peewee import Model, CharField, DecimalField, ForeignKeyField, DateTimeField
from datetime import datetime
from .db import db
from .user import User

class Product(Model):
    user = ForeignKeyField(User, backref='products')
    created_at = DateTimeField(default=datetime.now)
    income = DecimalField()

    class Meta:
        database = db