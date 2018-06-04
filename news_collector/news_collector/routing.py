from django.urls import path, re_path
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from collector.consumers import NewsCollectorAsyncConsumer


# By default, the ProtocolTypeRouter sets the "http" route to just be Django.
# This overrides it to send it to our asynchronous consumer for a single path,
# and to Django for all other pages.
application = ProtocolTypeRouter({
    "http": URLRouter([
        # Our async news fetcher
        path("collector/collect_news_async/", NewsCollectorAsyncConsumer),

        # AsgiHandler is "the rest of Django" - send things here to have Django
        # views handle them.
        re_path("^", AsgiHandler),
    ]),
})
