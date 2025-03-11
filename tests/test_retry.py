import asyncio
import unittest
from retry import retry, TooManyRetries


class TestRetryFunction(unittest.IsolatedAsyncioTestCase):

    async def test_retry_fails_with_too_many_retries(self):

        async def failing_task():
            raise Exception("Error!")

        with self.assertRaises(TooManyRetries):
            await retry(failing_task, max_retries=3, timeout=0.1, retry_interval=0.1)

    async def test_retry_succeeds_on_second_attempt(self):
        call_count = 0

        async def sometimes_failing_task():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Error!")
            return "Success"

        result = await retry(sometimes_failing_task, max_retries=3, timeout=0.1, retry_interval=0.1)
        self.assertEqual(result, "Success")
        self.assertEqual(call_count, 2)

    async def test_retry_timeout_raises_too_many_retries(self):

        async def slow_task():
            await asyncio.sleep(1)

        with self.assertRaises(TooManyRetries):
            await retry(slow_task, max_retries=3, timeout=0.1, retry_interval=0.1)

    async def test_retry_logs_exceptions(self):

        async def failing_task():
            raise Exception("Error!")

        with self.assertLogs("root", level="ERROR") as log:
            with self.assertRaises(TooManyRetries):
                await retry(failing_task, max_retries=3, timeout=0.1, retry_interval=0.1)
        self.assertTrue(any("An exception occurred while waiting" in message for message in log.output))


if __name__ == "__main__":
    unittest.main()
