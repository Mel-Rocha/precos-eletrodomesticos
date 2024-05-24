import os
import asyncio
from decimal import Decimal

from dotenv import load_dotenv
from tortoise import Tortoise

from apps.core.models import BackhoeTable

load_dotenv()


async def save_to_database(data):
    for item in data:
        existing_backhoe = await BackhoeTable.filter(url=item['url']).first()
        if existing_backhoe:
            price = item['price'].replace('R$ ', '').replace('.', '').replace(',', '.')
            if existing_backhoe.price != float(price):
                await create_new_backhoe(item)
        else:
            await create_new_backhoe(item)


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


async def init():
    await Tortoise.init(
        db_url=os.getenv('DATABASE_URL'),
        modules={'models': ['apps.core.models']}
    )

if __name__ == "__main__":
    data = [
        {
            'fabricator': 'NEW HOLLAND',
            'model': 'B95B',
            'year': '2011',
            'price': 'R$ 240.000,00',
            'worked_hours': None,
            'url': 'https://www.caminhoesecarretas.com.br/veiculo/aruja/sp/retro-escavadeira/new-holland/b95b/2012/tracao-4x4/cabine-fechada/cattrucks/1118497',
            'crawling_date': '2024-05-24 13:42:21'
        },
        {
            'fabricator': 'NEW HOLLAND',
            'model': 'B95B',
            'year': None,
            'price': 'R$ 240.000,00',
            'worked_hours': 100,
            'url': 'https://www.caminhoesecarretas.com.br/veiculo/aruja/sp/retro-escavadeira/new-holland/b95b/2012/tracao-4x4/cabine-fechada/cattrucks/1118494',
            'crawling_date': '2024-05-24 13:42:22'
        }
    ]
    asyncio.run(init())
    asyncio.run(save_to_database(data))