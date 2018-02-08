MultiChat
=========

Basic example of a multi-room chatroom, with messages from all rooms a user
is in multiplexed over a single WebSocket connection.

There is no chat persistence; you only see messages sent to a room while you
are in that room.

Uses the Django auth system to provide user accounts; users are only able to
use the chat once logged in, and this provides their username details for the
chatroom.

Some channels can be limited to only "staff" users; the example includes
code that checks user credentials on incoming WebSockets to allow or deny them
access to chatroom streams based on their staff status.


Installation
------------

Manual installation
~~~~~~~~~~~~~~~~~~~

Make a new virtualenv for the project, and run::

    pip install -r requirements.txt

Then, you'll need Redis running locally; the settings are configured to
point to ``localhost``, port ``6379``, but you can change this in the
``CHANNEL_LAYERS`` setting in ``settings.py``.

Finally, run::

    python manage.py migrate
    python manage.py runserver


Docker installation
~~~~~~~~~~~~~~~~~~~

Run the app::

    docker-compose up -d

The app will now be running on: {your-docker-ip}:8000

**Note:** You will need to prefix any ``python manage.py`` commands with: ``docker-compose run --rm web``. e.g.: ``docker-compose run --rm web python manage.py createsuperuser``

Finally, run::

    docker-compose run --rm web python manage.py migrate


Usage
-----

Make yourself a superuser account::

    python manage.py createsuperuser

Then, log into http://localhost:8000/admin/ and make a couple of Room objects.
Be sure to make one that is set to "staff-only",

Finally, make a second user account in the admin that doesn't have staff
privileges. You'll use this to log into the chat in a second window, and to test
the authentication on that staff-only room.

Now, open a second window in another browser or in "incognito" mode - you'll be
logging in to the same site with two user accounts. Navigate to
http://localhost:8000 in both browsers and open the same chatroom.

Now, you can type messages and see them appear on both screens at once. You can
join other rooms and try there, and see how you receive messages from all rooms
you've currently joined.

If you try and make the non-staff user join your staff-only chatroom, you should
see an error as the server-side authentication code kicks in.


How It Works
------------

There's a normal Django view that just serves a HTML page behind the normal
``@login_required`` decorator, and that is basically a single-page app with
all the JS loaded into the ``index.html`` file (as this is an example).

There's a single consumer, which you can see routed to in ``multichat/routing.py``,
which is wrapped in the Channels authentication ASGI middleware so it can check
that your user is logged in and retrieve it to check access as you ask to join
rooms.

Which rooms you are in is kept track of in ``self.rooms`` on the consumer
so they can be left cleanly if you disconnect.

Whenever the client asks to join a room, leave a room, or send a message,
it sends a WebSocket text frame with a JSON encoded command. We use a generic
consumer to handle decoding that JSON for us, and then dispatch to one of three
handler functions based on what the command is.

All rooms have an associated group, and for joins, leaves and messages, an
event is sent over the channel layer to that group. The consumers who are in
the group will receive those messages, and the consumer also has handler
functions for those (e.g. ``chat_join``), which it uses to encode the events
down into the WebSocket wire format before sending them to the client.


Suggested Exercises
-------------------

If you want to try out making some changes and getting a feel for Channels,
here's some ideas and hints on how to do them:

* Make messages from yourself have a different message type. You'll need to
  edit the ``chat_message`` function to send a different packet down to the
  client based on if the ``chat.message`` event it gets is from you or not.

* Add message persistence. There's already a message sent to make a user join
  a room, so you can use that to send some previous messages; you'll need to make
  a model to save messages in, though.

* Make the Room list dynamically change as rooms are added and removed.
  You could add a common group that every socket joins and send events to it
  as rooms are created/deleted.

* Add message editing and deletion. You'll need to have made them persistent
  first; make sure you send message IDs down with every message so the client can
  keep track of them. Then, write some code to handle editing and trigger
  sending new messages down when this happens with the message ID it's happening to.


Further Reading
---------------

You can find the Channels documentation at http://channels.readthedocs.org
