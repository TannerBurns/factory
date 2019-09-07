from rest_framework import serializers

from .models import Task, Session, Operation, Runtime, Content

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("created", "session_id")
        read_only_fields = ("created", "session_id")

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ("created", "name", "docstring")
        read_only_fields = ("created", "name", "docstring")

class RuntimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ("start", "stop", "runtime")
        read_only_fields = ("start", "stop", "runtime")

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
    session = SessionSerializer()
    operation = OperationSerializer()
    content = ContentSerializer()
    runtime = RuntimeSerializer()
    class Meta:
        model = Task
        fields = ("created", "task_id", "status", "session", "operation", "content", "runtime")

class TaskListSerializer(serializers.ModelSerializer):
    session = SessionSerializer()
    operation = OperationSerializer()
    runtime = RuntimeListSerializer()
    class Meta:
        model = Task
        fields = ("created", "task_id", "status", "session", "operation", "runtime")