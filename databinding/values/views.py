from django.shortcuts import render
from .models import IntegerValue


def index(request):
    """
    Root page view. Just shows a list of values currently available.
    """
    return render(request, "index.html", {
        "integer_values": IntegerValue.objects.order_by("id"),
    })

