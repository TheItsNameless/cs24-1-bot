from tortoise import Model, fields

from models.database.baseModel import BaseModel


class User(BaseModel):
    id = fields.IntField(pk=True, description="The ID of the user on Discord")
    global_name = fields.CharField(max_length=255, description="The name of the user on Discord")
    display_name = fields.CharField(
        max_length=255,
        description="The display name of the user on the Server")  # Maybe outdated because it is not updated on
    # every message

    def __str__(self):
        return self.display_name
