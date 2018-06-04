from django.urls import path
from collector.views import index
from collector.views import news_collector_sync_view


urlpatterns = [
    # Synchronous news collector
    path('collector/collect_news_sync/', news_collector_sync_view),
    path('', index),
]
