import uuid

from tortoise import fields, Model


class CoreTable(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    crawl_date = fields.DatetimeField(auto_now=True)
    fabricator = fields.CharField(max_length=255)
    model = fields.CharField(max_length=255)
    year_fabrication = fields.IntField(default=0)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    url = fields.CharField(max_length=255)
    worked_hours = fields.DecimalField(max_digits=5, decimal_places=2)
    state = fields.CharField(max_length=255)
    date_of_posting = fields.DatetimeField()
    is_combine_harvester = fields.BooleanField(default=True)  # Colheitadeira
    is_backhoe = fields.BooleanField(default=False)  # Retroescavadeira
    is_loader = fields.BooleanField(default=False)  # Pá Carregadeira
    is_small_loader = fields.BooleanField(default=False)  # Mini Carregadeira
    is_mini_excavator = fields.BooleanField(default=False)  # Mini Escavadeira
    is_crawler_tractor = fields.BooleanField(default=False)  # Trator Esteira

    class Meta:
        abstract = True



