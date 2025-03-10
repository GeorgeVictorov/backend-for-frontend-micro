import unittest
from unittest.mock import AsyncMock

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

import products


class ProductsHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app[products.DB_KEY] = AsyncMock()
        app.add_routes(products.routes)
        return app

    async def test_get_products_success(self):
        fake_data = [
            {"product_id": 1, "product_name": "Product A"},
            {"product_id": 2, "product_name": "Product B"}
        ]
        self.app[products.DB_KEY].fetch.return_value = fake_data

        response = await self.client.get("/products")

        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertEqual(json_data, fake_data)

    async def test_get_products_empty(self):
        self.app[products.DB_KEY].fetch.return_value = []

        response = await self.client.get("/products")

        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertEqual(json_data, [])


if __name__ == '__main__':
    unittest.main()
