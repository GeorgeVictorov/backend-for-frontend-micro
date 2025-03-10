import asyncpg
from aiohttp.web import Application
from asyncpg.pool import Pool

DB_KEY = 'database'

async def create_db_pool(app: Application,
                         host: str,
                         port: int,
                         user: str,
                         database: str,
                         password: str,):
    pool: Pool = await asyncpg.create_pool(host=host,
                                           port=port,
                                           user=user,
                                           database=database,
                                           password=password,
                                           min_size=6,
                                           max_size=6)
    app[DB_KEY] = pool

async def destroy_db_pool(app: Application):
    pool: Pool = await app[DB_KEY]
    await pool.close()