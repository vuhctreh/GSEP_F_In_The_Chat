""" Includes serializers which are used to convert the data
    sent in a HTTP request to a Django object and a Django object
    to a valid response data."""

from rest_framework import serializers
from app.models import Task


class TasksSerializer(serializers.ModelSerializer):
    """ Serializer that converts task data from an HTTP request to
        an object"""

    class Meta:
        """ Fields that comprise a task """
        model = Task
        fields = ('id', 'title', 'description', 'completed')
