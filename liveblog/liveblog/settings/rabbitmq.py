from .base import *

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_url = 'amqp://guest:guest@%s:5672/%%2F' % rabbitmq_host

# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Rabbitmq channel layer implementation asgi_rabbitmq
        "BACKEND": "asgi_rabbitmq.RabbitmqChannelLayer",
        "CONFIG": {
            "url": rabbitmq_url,
        },
        "ROUTING": "liveblog.routing.channel_routing",
    },
}
