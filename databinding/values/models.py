from django.db import models
from channels.binding.websockets import WebsocketBinding


class IntegerValue(models.Model):

    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(default=0)


class IntegerValueBinding(WebsocketBinding):

    model = IntegerValue
    stream = "intval"
    fields = ["name", "value"]

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["binding.values"]

    def has_permission(self, user, action, pk):
        return True
