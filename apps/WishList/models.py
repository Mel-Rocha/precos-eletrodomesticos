import uuid

from tortoise import fields, Model

CHOICES = [
    ('very_low', 'Very Low'),
    ('low', 'Low'),
    ('average', 'Average'),
    ('high', 'High'),
    ('very_high', 'Very High'),
]


class WishList(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    product_name = fields.CharField(max_length=255)
    site_domain = fields.CharField(max_length=255)
    expected_purchase_date = fields.DateField()
    desire_to_acquire = fields.CharField(max_length=10, choices=CHOICES, default='average')
    need_to_acquire = fields.CharField(max_length=10, choices=CHOICES, default='average')
