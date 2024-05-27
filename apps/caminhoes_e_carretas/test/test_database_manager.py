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
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.db_manager = DatabaseManager()
        cls.loop.run_until_complete(
            Tortoise.init(
                db_url=os.getenv('TEST_DATABASE_URL'),
                modules={'models': ['apps.core.models']}
            )
        )
        cls.loop.run_until_complete(BackhoeTable.all().delete())

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(Tortoise.close_connections())
        cls.loop.close()

    def test_save_to_database(self):
        # Caso de teste 1: URL inédita
        item = {
            'fabricator': 'NEW HOLLAND',
            'model': 'B95B',
            'year': '2011',
            'price': 'R$ 240.000,00',
            'worked_hours': None,
            'url': 'https://www.caminhoesecarretas.com.br/veiculo/aruja/sp/retro-escavadeira/new-holland/b95b/2012/tracao-4x4/cabine-fechada/cattrucks/1118497',
            'crawling_date': '2024-05-24 13:42:21'
        }
        with self.subTest(case='URL inédita'):
            self.loop.run_until_complete(self.db_manager.save_to_database([item]))
            saved_item = self.loop.run_until_complete(BackhoeTable.filter(url=item['url']).first())
            self.assertIsNotNone(saved_item, "Item was not saved to the database")

        # Caso de teste 2: URL existente com o mesmo preço
        item_same_price = item.copy()
        item_same_price['price'] = 'R$ 240.000,00'  # Mesmo preço
        item_same_price['crawling_date'] = '2024-05-25 13:42:22'  # Data de rastreamento mais recente
        with self.subTest(case='URL existente com o mesmo preço'):
            initial_count = self.loop.run_until_complete(BackhoeTable.all().count())
            self.loop.run_until_complete(self.db_manager.save_to_database([item_same_price]))
            final_count = self.loop.run_until_complete(BackhoeTable.all().count())
            self.assertEqual(initial_count, final_count, "A new item should not have been created")

        # Caso de teste 3: URL existente com preço diferente
        item_different_price = item.copy()
        item_different_price['price'] = 'R$ 250.000,00'
        with self.subTest(case='URL existente com preço diferente'):
            initial_count = self.loop.run_until_complete(BackhoeTable.all().count())
            self.loop.run_until_complete(self.db_manager.save_to_database([item_different_price]))
            final_count = self.loop.run_until_complete(BackhoeTable.all().count())
            self.assertEqual(initial_count + 1, final_count, "A new item should have been created")


if __name__ == '__main__':
    unittest.main()
