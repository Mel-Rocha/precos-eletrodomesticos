from decimal import Decimal

from apps.core.models import BackhoeTable


class DatabaseManager:

    @staticmethod
    async def get_current_record_count():
        return await BackhoeTable.all().count()

    @staticmethod
    async def save_to_database(data):
        for item in data:
            existing_backhoe = await BackhoeTable.filter(url=item['url']).first()
            if existing_backhoe:
                price = item['price'].replace('R$ ', '').replace('.', '').replace(',', '.')
                if existing_backhoe.price != float(price):
                    await DatabaseManager.create_new_backhoe(item)
            else:
                await DatabaseManager.create_new_backhoe(item)

    @staticmethod
    async def create_new_backhoe(item):
        price = item['price'].replace('R$ ', '').replace('.', '').replace(',', '.')
        backhoe = BackhoeTable(
            crawl_date=item['crawling_date'],
            fabricator=item['fabricator'],
            model=item['model'],
            url=item['url'],
            price=Decimal(price),
            worked_hours=float(item['worked_hours']) if item['worked_hours'] is not None else None,
            year_fabrication=int(item['year']) if item['year'] is not None else None,
        )
        await backhoe.save()

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
