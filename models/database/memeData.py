from enum import Enum

from tortoise import Model
from tortoise import fields

from models.database.baseModel import BaseModel
from models.database.userData import User


class MemeFormat(Enum):
    PNG = "png"
    GIF = "gif"


class Meme(BaseModel):
    uuid = fields.UUIDField(pk=True, description="The UUID of the meme image")
    format = fields.CharEnumField(MemeFormat, max_length=3, description="The format of the meme image")
    message = fields.TextField(description="The message that the user attached to the meme image")
    content = fields.TextField(description="The OCRed content of the meme image")
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="memes")
    date = fields.DatetimeField(description="The date the meme was sent")

    def __str__(self):
        return self.uuid
