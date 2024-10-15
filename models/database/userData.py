from tortoise import Model, fields

from models.database.baseModel import BaseModel


class User(BaseModel):
    id = fields.IntField(pk=True)
    global_name = fields.CharField(max_length=255)
    display_name = fields.CharField(max_length=255)  # Maybe outdated because it is not updated on every message

    def __str__(self):
        return self.display_name
