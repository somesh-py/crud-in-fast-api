from tortoise.models import Model
from tortoise import Tortoise,fields


class User(Model):
    id=fields.IntField(pk=True)
    email=fields.CharField(50,unique=True)
    name=fields.CharField(50)
    phone=fields.CharField(10)
    password=fields.CharField(250)


Tortoise.init_models(['app.models'],"models")