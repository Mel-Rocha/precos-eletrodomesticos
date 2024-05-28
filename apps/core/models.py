import uuid

from tortoise import fields, Model


class CoreTable(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    price = fields.BigIntField(index=True)
    url = fields.CharField(max_length=255, index=True)
    crawl_date = fields.DatetimeField(auto_now=True)
    description = fields.CharField(max_length=600, null=True)
    fabricator = fields.CharField(max_length=255, null=True)
    model = fields.CharField(max_length=255, null=True)
    year_fabrication = fields.IntField(null=True)
    worked_hours = fields.IntField(null=True)
    state = fields.CharField(max_length=255, null=True)
    date_of_posting = fields.DatetimeField(null=True)
    length = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    volume = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    pallets = fields.IntField(null=True)
    model_code = fields.CharField(max_length=50, null=True)

    class Meta:
        abstract = True


class BackhoeTable(CoreTable):
    pass
