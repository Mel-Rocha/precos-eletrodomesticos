from pytz import timezone
from tortoise.transactions import in_transaction

from apps.core.models import BackhoeTable


class DatabaseManager:

    @staticmethod
    async def get_current_record_count():
        return await BackhoeTable.all().count()

    @staticmethod
    async def save_to_database(data):
        async with in_transaction() as connection:
            items_to_create = []
            for item in data:
                existing_backhoe = await BackhoeTable.filter(url=item['url']).using_db(connection).first()
                if existing_backhoe:
                    if existing_backhoe.price != item['price']:
                        items_to_create.append(DatabaseManager.create_new_backhoe_instance(item))
                else:
                    items_to_create.append(DatabaseManager.create_new_backhoe_instance(item))

            if items_to_create:
                await BackhoeTable.bulk_create(items_to_create, using_db=connection)

    @staticmethod
    def create_new_backhoe_instance(item):
        return BackhoeTable(
            crawl_date=item['crawling_date'],
            fabricator=item['fabricator'],
            model=item['model'],
            url=item['url'],
            price=item['price'],
            worked_hours=item['worked_hours'],
            year_fabrication=item['year'],
        )

    @staticmethod
    async def save_data_and_get_new_record_count(data):
        initial_count = await DatabaseManager.get_current_record_count()
        await DatabaseManager.save_to_database(data)
        final_count = await DatabaseManager.get_current_record_count()
        return final_count - initial_count

    @staticmethod
    async def count_records_with_null_model_code():
        records_with_null_model_code = await BackhoeTable.filter(model_code=None).count()
        return records_with_null_model_code

    @staticmethod
    async def get_all_data():
        backhoes = await BackhoeTable.all().values()
        for backhoe in backhoes:
            backhoe['crawl_date'] = backhoe['crawl_date'].astimezone(timezone('America/Sao_Paulo')).replace(tzinfo=None)
        return backhoes
