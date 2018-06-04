import asyncio
import requests
import json
import datetime
from aiohttp import ClientSession
from django.conf import settings
from channels.generic.http import AsyncHttpConsumer
from .constants import BLOGS


class NewsCollectorAsyncConsumer(AsyncHttpConsumer):

    async def handle(self, body):

        # Adapted from:
        # "Making 1 million requests with python-aiohttp"
        # https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
        async def fetch(url, session):
            async with session.get(url) as response:
                return await response.read()

        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        t0 = datetime.datetime.now()
        async with ClientSession() as session:
            for name, url in BLOGS.items():
                print('Start downloading "%s"' % name)
                task = asyncio.ensure_future(fetch(url, session))
                tasks.append(task)

            # gather all responses
            responses = await asyncio.gather(*tasks)
            dt = (datetime.datetime.now() - t0).total_seconds()
            print(f'All downloads completed; elapsed time: {dt} [s]')

        # Here, we assume that the responses have been gathered
        # in the same order as the original task list. Is this correct ?
        data = dict(zip(BLOGS.keys(), [r.decode('utf-8') for r in responses]))
        text = json.dumps(data)

        await self.send_response(200,
            text.encode(),
            headers=[
                ("Content-Type", "application/json"),
            ]
        )
