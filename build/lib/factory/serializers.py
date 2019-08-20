from rest_framework import serializers

from .models import Tasks

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ("created", "task_id", "session", "name", "status",)
        read_only_fields = ("created", "task_id", "session", "name", "status")

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ("created", "task_id", "session", "name", "status", "errors", "results")
        read_only_fields = ("created", "task_id", "session", "name", "status", "errors", "results")