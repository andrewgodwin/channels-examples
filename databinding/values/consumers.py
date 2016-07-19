from channels.generic.websockets import WebsocketDemultiplexer


class Demultiplexer(WebsocketDemultiplexer):

    mapping = {
        "intval": "binding.intval",
    }

    def connection_groups(self):
        return ["binding.values"]
