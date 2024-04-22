import uuid

from tortoise import fields, Model


class Product(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)  # Create logic to be false if there is no corresponding WishList
    # object
    name = fields.CharField(max_length=255)
    store = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255, null=True)
    price = fields.JSONField(default={})
