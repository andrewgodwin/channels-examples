from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import index


urlpatterns = [
    url(r'^$', index),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^admin/', admin.site.urls),
]
