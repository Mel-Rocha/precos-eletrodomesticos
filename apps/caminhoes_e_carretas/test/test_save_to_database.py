import asyncio
import unittest

from apps.core.models import BackhoeTable
from apps.caminhoes_e_carretas.db_manager import save_to_database, init


class TestSaveToDatabase(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(init())

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
        self.loop.run_until_complete(save_to_database(data))

        for item in data:
            with self.subTest(item=item):
                saved_item = self.loop.run_until_complete(BackhoeTable.filter(url=item['url']).first())
                self.assertIsNotNone(saved_item, "Item was not saved to the database")


if __name__ == '__main__':
    unittest.main()
