import uuid

from tortoise import fields, Model


class CoreTable(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    price = fields.BigIntField(index=True)
    url = fields.CharField(max_length=255, index=True)
    crawl_date = fields.DatetimeField(auto_now=True)
    product = fields.CharField(max_length=255, null=True)
    # description = fields.CharField(max_length=600, null=True)
    # brand = fields.CharField(max_length=255, null=True)
    # category = fields.CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class IkesakiTable(CoreTable):
    pass
