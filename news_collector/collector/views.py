import datetime
import requests
from django.shortcuts import render
from django.http import JsonResponse
from .constants import BLOGS


def index(request):
    """
    Main page is just a template
    """
    return render(request, "index.html", {})


def news_collector_sync_view(request):
    """
    Synchronous HTTP fetcher
    """

    data = {}
    t0 = datetime.datetime.now()
    max_dt = 0

    # Go through each blog and fetch it using requests
    for name, link in BLOGS.items():
        t1 = datetime.datetime.now()
        response = requests.get(link)
        if response.status_code != 200:
            data[name] = 'Download error'
        else:
            data[name] = response.content.decode("utf-8")
        dt = (datetime.datetime.now() - t1).total_seconds()
        print('Downloaded "{}" from "{}" in {} [s]'.format(name, link, dt))
        max_dt = max(dt, max_dt)

    # Work out total time
    dt = (datetime.datetime.now() - t0).total_seconds()
    print('All downloads completed; elapsed time: {} [s]'.format(dt))
    print('Slowest download required: {} [s]'.format(max_dt))

    return JsonResponse(data)
