from django.db import models
from channels import Channel, Group


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user):
        """
        Called to send a message to the room on behalf of a user.
        """
        # Send the message to the generic "message handling" channel; a consumer
        # will get it and convert it into websocket sends on the Group.
        # This isn't entirely necessary here, but could be useful if you want
        # to dispatch to multiple different subsystems on multiple channels
        Channel("chat_messages").send({
            "room": str(self.id),
            "message": message,
            "username": user.username,
        })
