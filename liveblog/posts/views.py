from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Liveblog


def index(request):
    """
    Root page view. Just shows a list of liveblogs.
    """
    # Get a list of liveblogs, ordered by the date of their most recent
    # post, descending (so ones with stuff happening are at the top)
    liveblogs = Liveblog.objects.annotate(
        max_created=Max("posts__created")
    ).order_by("-max_created")

    # Render that in the index template
    return render(request, "index.html", {
        "liveblogs": liveblogs,
    })


def liveblog(request, slug):
    """
    Shows an individual liveblog page.
    """
    # Get the liveblog by slug
    blog = get_object_or_404(Liveblog, slug=slug)

    # Render it with the posts ordered in descending order.
    # If the user has JavaScript enabled, the template has JS that will
    # keep it updated.
    return render(request, "liveblog.html", {
        "liveblog": blog,
        "posts": blog.posts.order_by("-created"),
    })
