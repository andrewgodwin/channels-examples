import asyncio
import json
import datetime
from aiohttp import ClientSession
from channels.generic.http import AsyncHttpConsumer
from .constants import BLOGS


class NewsCollectorAsyncConsumer(AsyncHttpConsumer):
    """
    Async HTTP consumer that fetches URLs.
    """

    async def handle(self, body):

        # Adapted from:
        # "Making 1 million requests with python-aiohttp"
        # https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
        async def fetch(url, session):
            async with session.get(url) as response:
                return await response.read()

        tasks = []
        loop = asyncio.get_event_loop()

        # aiohttp allows a ClientSession object to link all requests together
        t0 = datetime.datetime.now()
        async with ClientSession() as session:
            for name, url in BLOGS.items():
                print('Start downloading "%s"' % name)
                # Launch a coroutine for each URL fetch
                task = loop.create_task(fetch(url, session))
                tasks.append(task)

            # Wait on, and then gather, all responses
            responses = await asyncio.gather(*tasks)
            dt = (datetime.datetime.now() - t0).total_seconds()
            print('All downloads completed; elapsed time: {} [s]'.format(dt))

        # asyncio.gather returns results in the order of the original sequence,
        # so we can safely zip these together.
        data = dict(zip(BLOGS.keys(), [r.decode('utf-8') for r in responses]))
        text = json.dumps(data)

        # We have to send a response using send_response rather than returning
        # it in Channels' async HTTP consumer
        await self.send_response(200,
            text.encode(),
            headers=[
                (b"Content-Type", b"application/json"),
            ]
        )
