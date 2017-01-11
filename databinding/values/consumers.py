from channels.generic.websockets import WebsocketDemultiplexer

from .models import IntegerValueBinding


class Demultiplexer(WebsocketDemultiplexer):
    consumers = {
        "intval": IntegerValueBinding.consumer,
    }

    groups = ["binding.values"]
