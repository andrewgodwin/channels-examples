import datetime
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import JsonResponse
from .constants import BLOGS


def index(request):
    return render(request, "index.html", {
    })


def news_collector_sync_view(request):

    data = {}
    t0 = datetime.datetime.now()
    max_dt = 0

    for name, link in BLOGS.items():
        t1 = datetime.datetime.now()
        response = requests.get(link)
        if response.status_code != 200:
            data[name] = 'Download error'
        else:
            data[name] = response.content.decode("utf-8")
        dt = (datetime.datetime.now() - t1).total_seconds()
        print(f'Downloaded "{name}" from "{link}" in {dt} [s]')
        max_dt = max(dt, max_dt)

    dt = (datetime.datetime.now() - t0).total_seconds()
    print(f'All downloads completed; elapsed time: {dt} [s]')
    print(f'Slowest download required: {max_dt} [s]')

    return JsonResponse(data)
