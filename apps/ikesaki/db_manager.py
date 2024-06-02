from pytz import timezone
from tortoise.transactions import in_transaction

from apps.core.models import IkesakiTable


class DatabaseManager:

    @staticmethod
    async def get_current_record_count():
        return await IkesakiTable.all().count()

    @staticmethod
    async def save_to_database(data):
        async with in_transaction() as connection:
            items_to_create = []
            for item in data:
                existing_backhoe = await IkesakiTable.filter(url=item['url']).using_db(connection).first()
                if existing_backhoe:
                    if existing_backhoe.price != item['price']:
                        items_to_create.append(DatabaseManager.create_new_backhoe_instance(item))
                else:
                    items_to_create.append(DatabaseManager.create_new_backhoe_instance(item))

            if items_to_create:
                await IkesakiTable.bulk_create(items_to_create, using_db=connection)

    @staticmethod
    def create_new_backhoe_instance(item):
        return IkesakiTable(
            crawl_date=item['crawling_date'],
            url=item['url'],
            price=item['price'],
            product=item['product']
        )

    @staticmethod
    async def save_data_and_get_new_record_count(data):
        initial_count = await DatabaseManager.get_current_record_count()
        await DatabaseManager.save_to_database(data)
        final_count = await DatabaseManager.get_current_record_count()
        return final_count - initial_count

    @staticmethod
    async def get_all_data():
        backhoes = await IkesakiTable.all().values()
        for backhoe in backhoes:
            backhoe['crawl_date'] = backhoe['crawl_date'].astimezone(timezone('America/Sao_Paulo')).replace(tzinfo=None)
        return backhoes
