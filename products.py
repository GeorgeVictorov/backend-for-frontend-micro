import functools

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from config import load_config
from db import DB_KEY, create_db_pool, destroy_db_pool

config = load_config()
routes = web.RouteTableDef()


@routes.get('/products')
async def products(request: Request) -> Response:
    db = request.app[DB_KEY]
    product_query = 'SELECT product_id, product_name FROM product'
    result = await db.fetch(product_query)
    return web.json_response(dict(record) for record in result)


app = web.Application()
app.on_startup.append(functools.partial(create_db_pool,
                                        host=config.db.host,
                                        port=5432,
                                        user=config.db.username,
                                        password=config.db.password,
                                        database='products'
                                        ))
app.on_cleanup.append(destroy_db_pool)
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8000)
