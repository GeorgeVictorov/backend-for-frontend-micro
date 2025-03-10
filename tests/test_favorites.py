import unittest
from unittest.mock import AsyncMock

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

import favorites


class FavoritesHandlerTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app[favorites.DB_KEY] = AsyncMock()
        app.add_routes(favorites.routes)
        return app

    async def test_favorites_success(self):
        fake_data = [{"product_id": 101}, {"product_id": 202}]
        self.app[favorites.DB_KEY].fetch.return_value = fake_data

        response = await self.client.get("/users/1/favorites")
        self.assertEqual(response.status, 200)
        json_data = await response.json()
        self.assertEqual(json_data, fake_data)

    async def test_favorites_not_found(self):
        self.app[favorites.DB_KEY].fetch.return_value = []
        response = await self.client.get("/users/1/favorites")
        self.assertEqual(response.status, 404)

    async def test_favorites_invalid_user_id(self):
        response = await self.client.get("/users/abc/favorites")
        self.assertEqual(response.status, 400)


if __name__ == '__main__':
    unittest.main()
