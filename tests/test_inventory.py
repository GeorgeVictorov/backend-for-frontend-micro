import unittest
from unittest.mock import patch

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

import inventory


class InventoryHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.add_routes(inventory.routes)
        return app

    @patch('random.randint')
    @patch('asyncio.sleep', return_value=None)
    async def test_inventory_success(self, mock_sleep, mock_randint):
        mock_randint.side_effect = [0, 100]

        response = await self.client.get('/products/1/inventory')

        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertEqual(json_data, {'inventory': 100})
        mock_sleep.assert_called_once_with(0)

    async def test_inventory_random(self):
        response = await self.client.get('/products/1/inventory')

        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertIn('inventory', json_data)


if __name__ == '__main__':
    unittest.main()
