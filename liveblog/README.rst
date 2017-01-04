Liveblog
========

Illustrates a "liveblog" using Channels. This is a page that shows a series
of short-form posts in descending date order, with new ones appearing at the
top as they're posted.

The site supports multiple liveblogs at once, and clients only listen for new
posts on the blog they're currently viewing.

When you view a liveblog page, we open a WebSocket to Django, and the consumer
there adds it to a Group based on the liveblog slug it used in the URL of the
socket. Then, in the ``save()`` method of the ``Post`` model, we send notifications
onto that Group that all currently connected clients pick up on, and insert
the new post at the top of the page.

Updates are also supported - the notification is sent with an ID, and if a post
with that ID is already on the page, the JavaScript just replaces its content
instead.


Installation
------------

Manual installation
~~~~~~~~~~~~~~~~~~~

Make a new virtualenv for the project, and run::

    pip install -r requirements/redis.txt

Then, you'll need Redis running locally; the settings are configured to
point to ``localhost``, port ``6379``, but you can change this in the
``CHANNEL_LAYERS`` setting in ``settings.py``.

Finally, run::

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Docker installation
~~~~~~~~~~~~~~~~~~~

Run the app::

    docker-compose up -d

You can omit the `-d` if you want to have the container log directly to
your terminal.   You can always see the logs with::

    docker-compose logs web

The app will now be running on: http://{your-docker-ip}:8000

The migration is done as part of the Dockerfile and shouldn't need to be
repeated (but it's ok to do so if you get an error).

Then create the superuser::

    docker-compose run --rm web python manage.py createsuperuser

Usage
-----

For Docker, replace `localhost` below with `{your-docker-ip}`.

Then, log into http://localhost:8000/admin/ and make a new Liveblog object.

Open a new window, go to http://localhost:8000/, and click on your new liveblog
to see its posts page.

Now, in the admin, make some new Posts against your blog, and watch them appear
in your new window. Edit them, and they'll update themselves live on the page too.

RabbitMQ
--------

You can try to run this example on RabbitMQ channel layer.

For manual installation use following commands::

    pip install -r requirements/rabbitmq.txt
    export DJANGO_SETTINGS_MODULE="liveblog.settings.rabbitmq"
    export PYTHONPATH=$PWD
    django-admin migrate
    django-admin createsuperuser
    django-admin runworker
    daphne -b 0.0.0.0 -p 8000 liveblog.asgi:channel_layer

For docker installation use::

    docker-compose -f docker-compose.rabbitmq.yml run --rm web django-admin migrate
    docker-compose -f docker-compose.rabbitmq.yml run --rm web django-admin createsuperuser
    docker-compose -f docker-compose.rabbitmq.yml up -d

The rest of necessary steps are the same.

Suggested Exercises
-------------------

If you want to try out making some changes and getting a feel for Channels,
here's some ideas and hints on how to do them:

* Make the posts disappear immediately on post deletion. You'll need to send
  notifications triggered on the model delete, in a similar way to the ones
  for save, and modify the JavaScript to understand them.

* Implement a view of all liveblogs at once. You'll need to make a new group
  that people who connect to this endpoint will subscribe to, insert into that
  group from the save() method as well as the existing per-liveblog group,
  and make new consumers to add and remove people from that group as they
  connect to a WebSocket on a different path (including new routing entries).

* Make the front page list of liveblogs update. You'll need another new WebSocket
  endpoint (with new consumers and routing), a new group to send updates down,
  and to tie that group into LiveBlog's save process. Decide if you want to
  send differential updates, or just re-send the whole list each time a new one
  is created. Both have advantages - what are they?

* Try adding Like functionality to the posts, so viewers can "like" a post and
  it's sent back over the WebSocket to a ``websocket.receive`` consumer that
  saves the like into the database, then propagates it to all existing clients.
  Can you reuse the existing Post.save() hook? What happens if hundreds
  of people are trying to like every second?


Further Reading
---------------

You can find the Channels documentation at http://channels.readthedocs.org
