import json
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room


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


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    # Initialise their session
    message.channel_session['rooms'] = []


# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low-level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
@channel_session_user
def ws_receive(message):
    # See if the message is a chat message, or a room join/leave request
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    try:
        if "join" in payload:
            # Find the room they requested (by ID) and add ourselves to the send group
            # Note that, because of channel_session_user, we have a message.user
            # object that works just like request.user would. Security!
            room = get_room_or_error(payload["join"], message.user)
            # OK, add them in. The websocket_group is what we'll send messages
            # to so that everyone in the chat room gets them.
            room.websocket_group.add(message.reply_channel)
            message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
            # Send a message back that will prompt them to open the room
            # Done server-side so that we could, for example, make people
            # join rooms automatically.
            message.reply_channel.send({
                "text": json.dumps({
                    "join": str(room.id),
                    "title": room.title,
                }),
            })
        elif "leave" in payload:
            # Reverse of join - remove them from everything.
            room = get_room_or_error(payload["leave"], message.user)
            room.websocket_group.discard(message.reply_channel)
            message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
            # Send a message back that will prompt them to close the room
            message.reply_channel.send({
                "text": json.dumps({
                    "leave": str(room.id),
                }),
            })
        elif "send" in payload:
            # Find the room they're sending to, check perms
            room = get_room_or_error(payload["send"][0], message.user)
            # Send the message along
            room.send_message(payload["send"][1], message.user)
        else:
            raise ClientError("UNKNOWN_COMMAND")
    except ClientError as e:
        # If we catch a client error, tell it to send an error string
        # back to the client on their reply channel
        e.send_to(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            # Removes us from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


def handle_chat_message(message):
    """
    Called when a message goes via Room.send_message onto the "messages" channel.
    Encodes the message into a WebSocket response and sends it out.
    This could be inlined in the model, but I wanted to illustrate custom channels
    and also try to keep all the protocol code in the one place.
    """
    # Message.content is the raw dictionary of what the message contains, i.e.
    # exactly what we sent onto the channel in Room.send_message
    room = Room.objects.get(pk=message['room'])
    room.websocket_group.send({
        "text": json.dumps(message.content),
    })


def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    # Check permissions
    if room.staff_only and not user.is_staff:
        raise ClientError("ROOM_ACCESS_DENIED")
    return room
