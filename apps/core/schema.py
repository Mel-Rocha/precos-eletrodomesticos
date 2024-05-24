from tortoise.contrib.pydantic import pydantic_model_creator

from apps.core.models import BackhoeTable

BackhoeTableSchemaWithotFormattedDates = None


def initialize_backhoe_table_schema():
    global BackhoeTableSchemaWithotFormattedDates
    BackhoeTableSchemaWithotFormattedDates = pydantic_model_creator(BackhoeTable, exclude=('created_at',
                                                                                           'updated_at'))


initialize_backhoe_table_schema()


class BackhoeTableSchema(BackhoeTableSchemaWithotFormattedDates):
    formatted_created_at: str
    formatted_updated_at: str

    class Config:
        orm_mode = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatted_created_at = self.created_at.strftime('%d/%m/%Y %H:%M:%S') if self.created_at else None
        self.formatted_updated_at = self.updated_at.strftime('%d/%m/%Y %H:%M:%S') if self.updated_at else None
