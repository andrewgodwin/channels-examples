from django.conf.urls import url
from django.contrib import admin
from posts.views import index, liveblog


urlpatterns = [
    url(r'^$', index),
    url(r'^liveblog/(?P<slug>[^/]+)/$', liveblog),
    url(r'^admin/', admin.site.urls),
]
