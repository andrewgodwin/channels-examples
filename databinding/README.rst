Databinding
===========

Basic illustration of the Channels data binding framework, which allows you
to easily tie model changes to WebSockets for bidirectional binding with
JavaScript user interfaces.

It has just an IntegerValue model, which has a name and a value. The example
exposes each value as a slider on the root page, which when moved immediately
databinds the change back into the Django model, and which updates immediately
as the Django model is changed to reflect the new value.

Open as many windows as you like of the root page and move the sliders,
and all will immediately update to the current value. You can even edit the
values in the admin and the values will change as soon as you hit save.

Installation
------------

Manual installation
~~~~~~~~~~~~~~~~~~~~~~

Make a new virtualenv for the project, and run::

    pip install -r requirements.txt

Then, you'll need Redis running locally; the settings are configured to
point to ``localhost``, port ``6379``, but you can change this in the
``CHANNEL_LAYERS`` setting in ``settings.py``.


Finally, run::

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Docker installation
~~~~~~~~~~~~~~~~~~~~~~

Run the app::

    docker-compose up -d

The app will now be running on: http://{your-docker-ip}:8000

The migration is done as part of the Dockerfile and shouldn't need to be
repeated (but it's ok to do so if you get an error).

If migration required you can run::

    docker-compose run --rm web python manage.py migrate

Then create the superuser::

    docker-compose run --rm web python manage.py createsuperuser


Usage
-----
For Docker, replace `localhost` below with `{your-docker-ip}`.

Then, log into http://localhost:8000/admin/ and make some new Integer Values.

Open several new windows, point them all to http://localhost:8000/, and move
the sliders and see how the others update in real time as you change the values.

Edit the values through the admin view, and see how the sliders update to match
as soon as you hit save.


Suggested Exercises
-------------------

If you want to try out making some changes and getting a feel for Channels,
here's some ideas and hints on how to do them:

* Add the ability to create and delete integer values from the slider page
  using inbound data binding. The Django side of this is already complete;
  you just need to make the JavaScript send "create" actions with data and
  "delete" actions with a PK.

* Implement permission checking on the sliders, by overriding the has_permission
  method on the binding. You wouldn't want an insecure update mechanism
  would you?

* Make a page for each value that listens on a group just for that value's ID.
  You'll need new incoming WebSocket URLs, a dynamic group_names method on
  the binding that takes the PK in the path into account, and a tweak to the
  JavaScript to use the new URLs.


Further Reading
---------------

You can find the Channels documentation at http://channels.readthedocs.org
