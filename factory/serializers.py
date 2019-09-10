from rest_framework import serializers

from .models import Task, Operation, Runtime, Content

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ("created", "sha256", "name", "docstring")
        read_only_fields = ("created", "sha256", "name", "docstring")

class RuntimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ("created", "start", "stop", "total")
        read_only_fields = ("created", "start", "stop", "total")

class RuntimeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ("created", "start",)
        read_only_fields = ("created", "start",) 

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("created", "errors", "results")
        read_only_fields = ("created", "errors", "results")

class TaskSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    content = ContentSerializer(many=True)
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
