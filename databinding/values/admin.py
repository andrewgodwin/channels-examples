from django.contrib import admin
from .models import IntegerValue


admin.site.register(
    IntegerValue,
    list_display=["id", "name", "value"],
)
