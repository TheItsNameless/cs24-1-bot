from enum import Enum

from tortoise import Model
from tortoise import fields

from models.database.baseModel import BaseModel
from models.database.userData import User


class MemeFormat(Enum):
    PNG = "png"
    GIF = "gif"


class Meme(BaseModel):
    uuid = fields.UUIDField(pk=True)
    format = fields.CharEnumField(MemeFormat, max_length=3)
    message = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="memes")
    date = fields.DatetimeField()

    def __str__(self):
        return self.uuid
