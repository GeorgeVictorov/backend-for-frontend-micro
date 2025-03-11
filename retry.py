import asyncio
import logging
from typing import Awaitable, Callable


class TooManyRetries(Exception):
    pass


async def retry(coro: Callable[[], Awaitable],
                max_retries: int,
                timeout: float,
                retry_interval: float):
    for retry in range(max_retries):
        try:
            return await asyncio.wait_for(coro(), timeout=timeout)
        except Exception as e:
            logging.exception(f'An exception occurred while waiting (retry num: {retry}), retrying...', exc_info=e)
            await asyncio.sleep(retry_interval)

    raise TooManyRetries()
