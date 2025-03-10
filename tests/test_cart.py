import unittest
from unittest.mock import AsyncMock

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
import cart


class CartHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app[cart.DB_KEY] = AsyncMock()
        app.add_routes(cart.routes)
        return app

    async def test_get_cart_success(self):
        fake_data = [{"product_id": 101}, {"product_id": 202}]
        self.app[cart.DB_KEY].fetch.return_value = fake_data

        response = await self.client.get("/users/1/cart")

        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertEqual(json_data, fake_data)

    async def test_get_cart_not_found(self):
        self.app[cart.DB_KEY].fetch.return_value = []

        response = await self.client.get("/users/5/cart")

        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertEqual(json_data, [])

    async def test_get_cart_invalid_user_id(self):
        response = await self.client.get("/users/abc/cart")

        self.assertEqual(response.status, 400)

    async def test_get_cart_db_error(self):
        self.app[cart.DB_KEY].fetch.side_effect = Exception("Database error")

        response = await self.client.get("/users/1/cart")

        self.assertEqual(response.status, 500)  # Ошибка сервера


if __name__ == '__main__':
    unittest.main()
