import os
import asyncio
import unittest

from tortoise import Tortoise
from dotenv import load_dotenv

from apps.core.models import BackhoeTable
from apps.caminhoes_e_carretas.db_manager import DatabaseManager

load_dotenv()


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.db_manager = DatabaseManager()
        cls.loop.run_until_complete(
            Tortoise.init(
                db_url=os.getenv('DATABASE_URL'),
                modules={'models': ['apps.core.models']}
        )
        )

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(Tortoise.close_connections())
        cls.loop.close()

    def test_save_to_database(self):
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
            self.loop.run_until_complete(self.db_manager.save_to_database(data))

            for item in data:
                with self.subTest(item=item):
                    saved_item = self.loop.run_until_complete(BackhoeTable.filter(url=item['url']).first())
                    self.assertIsNotNone(saved_item, "Item was not saved to the database")


if __name__ == '__main__':
    unittest.main()
