import asyncio
import random

from aiohttp import web
from aiohttp.web_request import Request

routes = web.RouteTableDef()


@routes.get('/products/{id}/inventory')
async def get_inventory(request: Request):
    delay: int = random.randint(0, 5)
    await asyncio.sleep(delay)
    inventory: int = random.randint(0, 100)
    return web.json_response({'inventory': inventory})


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8001)
