import functools

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from config import load_config
from db import DB_KEY, create_db_pool, destroy_db_pool

config = load_config()
routes = web.RouteTableDef()


@routes.get('/users/{id}/cart')
async def favorites(request: Request) -> Response:
    try:
        str_id = request.match_info['id']
        user_id = int(str_id)
        db = request.app[DB_KEY]
        favorite_query = 'SELECT product_id from user_cart where user_id = $1'
        result = await db.fetch(favorite_query, user_id)
        if result:
            return web.json_response(dict(record) for record in result)
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()


app = web.Application()
app.on_startup.append(functools.partial(create_db_pool,
                                        host=config.db.host,
                                        port=5432,
                                        user=config.db.username,
                                        password=config.db.password,
                                        database='cart'
                                        ))
app.on_cleanup.append(destroy_db_pool)
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8003)
