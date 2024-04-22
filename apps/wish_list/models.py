import uuid

from tortoise import fields, Model

CHOICES = [
    (u'1', 'very_low'),
    (u'2', 'low'),
    (u'3', 'average'),
    (u'4', 'high'),
    (u'5', 'very_high')
]


class WishList(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    wish_title = fields.CharField(max_length=255, unique=True)
    expected_purchase_date = fields.DateField()
    desire_to_acquire = fields.CharField(max_length=10, choices=CHOICES, default='3')
    need_to_acquire = fields.CharField(max_length=10, choices=CHOICES, default='3')
    product_id = fields.UUIDField(null=True)
