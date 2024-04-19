import uuid

from tortoise import fields, Model


class ShoppingCart(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    product = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    store = fields.CharField(max_length=50)
    description = fields.CharField(max_length=255, blank=True, null=True)