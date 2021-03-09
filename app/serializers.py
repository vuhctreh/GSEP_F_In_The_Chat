""" Placeholder """

from rest_framework import serializers
from app.models import Task


class TasksSerializer(serializers.ModelSerializer):
    """ Placeholder """

    class Meta:
        """ Placeholder """
        model = Task
        fields = ('id', 'title', 'description', 'completed')
