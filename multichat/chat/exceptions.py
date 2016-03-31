import json


class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super(ClientError, self).__init__(code)
        self.code = code

    def send_to(self, channel):
        channel.send({
            "text": json.dumps({
                "error": self.code,
            }),
        })
