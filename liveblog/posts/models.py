import json
from django.db import models
from django.template.defaultfilters import linebreaks_filter
from django.utils.six import python_2_unicode_compatible
from channels import Group


@python_2_unicode_compatible
class Liveblog(models.Model):
    """
    A liveblog - a collection of posts under a title, like the event name that's
    being blogged.
    """

    # Liveblog title
    title = models.CharField(max_length=255)

    # Slug for routing (both HTML pages and WebSockets)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to view the liveblog.
        """
        return "/liveblog/%s/" % self.slug

    @property
    def group_name(self):
        """
        Returns the Channels Group name to use for sending notifications.
        """
        return "liveblog-%s" % self.id


@python_2_unicode_compatible
class Post(models.Model):
    """
    A single post in a liveblog; they'll be shown in descending date order,
    and new ones will appear at the top of the page as they're posted.
    """

    # Link back to the main blog.
    liveblog = models.ForeignKey(
        Liveblog,
        related_name="posts",
        on_delete=models.CASCADE,
    )

    # Body content of this post. It'll have the linebreaks filter run on it,
    # but nothing else. You could change this to be HTML/RST/Markdown etc.
    body = models.TextField()

    # Post and update times. I use auto_now_* here because I'm lazy.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#%i: %s" % (self.id, self.body_intro())

    def body_intro(self):
        """
        Short first part of the body to show in the admin or other compressed
        views to give you some idea of what this is.
        """
        return self.body[:50]

    def html_body(self):
        """
        Returns the rendered HTML body to show to browsers.
        You could change this method to instead render using RST/Markdown,
        or make it pass through HTML directly (but marked safe).
        """
        return linebreaks_filter(self.body)

    def send_notification(self):
        """
        Sends a notification to everyone in our Liveblog's group with our
        content.
        """
        # Make the payload of the notification. We'll JSONify this, so it has
        # to be simple types, which is why we handle the datetime here.
        notification = {
            "id": self.id,
            "html": self.html_body(),
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }
        # Encode and send that message to the whole channels Group for our
        # liveblog. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        Group(self.liveblog.group_name).send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(notification),
        })

    def save(self, *args, **kwargs):
        """
        Hooking send_notification into the save of the object as I'm not
        the biggest fan of signals.
        """
        result = super(Post, self).save(*args, **kwargs)
        self.send_notification()
        return result
