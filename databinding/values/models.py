import json
from django.db import models
from channels.binding.websockets import WebsocketBinding


class IntegerValue(models.Model):

    name = models.CharField(max_length=100, unique=True)
    value = models.IntegerField(default=0)


class IntegerValueBinding(WebsocketBinding):

    model = IntegerValue

    def serialize_data(self, instance):
        return {"name": instance.name, "value": instance.value}

    def group_names(self, instance, action):
        return ["binding.values"]

    def has_permission(self, user, action, pk):
        return True

    def create(self, data):
        self.model.objects.create(name=data['name'], value=data['value'])

    def update(self, instance, data):
        if "name" in data:
            instance.name = data['name']
        if "value" in data:
            instance.value = data['value']
        instance.save()
