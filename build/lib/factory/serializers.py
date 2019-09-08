from rest_framework import serializers

from .models import Task, Operation, Runtime, Content

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ("created", "name", "docstring", "sha256")
        read_only_fields = ("created", "name", "docstring", "sha256")

class RuntimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ("start", "stop", "total")
        read_only_fields = ("start", "stop", "total")

class RuntimeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ("start",)
        read_only_fields = ("start",)

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("created", "errors", "results")
        read_only_fields = ("created", "errors", "results")

class TaskSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    content = ContentSerializer()
    runtime = RuntimeSerializer()
    class Meta:
        model = Task
        fields = ("created", "task", "status", "session", "operation", "content", "runtime")

class TaskListSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    runtime = RuntimeListSerializer()
    class Meta:
        model = Task
        fields = ("created", "task", "status", "session", "operation", "runtime")
