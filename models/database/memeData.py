from tortoise import Model
from tortoise import fields

from models.database.baseModel import BaseModel
from models.database.userData import User


class Meme(BaseModel):
    uuid = fields.UUIDField(pk=True)
    message = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="memes")
    date = fields.DatetimeField()

    def __str__(self):
        return self.uuid
