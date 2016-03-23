from django.contrib import admin
from .models import Liveblog, Post


admin.site.register(
    Liveblog,
    list_display=["id", "title", "slug"],
    list_display_links=["id", "title"],
    ordering=["title"],
    prepopulated_fields={"slug": ("title",)},
)


admin.site.register(
    Post,
    list_display=["id", "liveblog", "created", "body_intro"],
    ordering=["-id"],
)
