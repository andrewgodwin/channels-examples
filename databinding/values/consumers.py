from channels.binding.websockets import WebsocketBindingDemultiplexer

from .models import IntegerValueBinding


class BindingConsumer(WebsocketBindingDemultiplexer):
    """
    This consumer does two things:
     - Adds people to the "binding.values" group when they join using the
       connection_groups feature of the class-based WebSocket consumers
     - Dispatches incoming binding updates to the right place by inheriting
       from the demultiplexer class and specifying the bindings list.
    """

    bindings = [
        IntegerValueBinding,
    ]

    def connection_groups(self):
        return ["binding.values"]
