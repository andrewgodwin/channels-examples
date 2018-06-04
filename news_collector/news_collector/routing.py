from django.urls import path, re_path
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from collector.consumers import NewsCollectorAsyncConsumer


application = ProtocolTypeRouter({
    "http": URLRouter([
        path("collector/collect_news_async/", NewsCollectorAsyncConsumer),
        re_path("^", AsgiHandler),
    ]),
})
