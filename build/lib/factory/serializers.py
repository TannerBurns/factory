from rest_framework import serializers

from .models import Task, Operation, Runtime, Content, Input, Output

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

class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ("created", "sha256", "type", "count")
        read_only_fields = ("created", "sha256", "type", "count")

class InputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ("created", "sha256", "count")
        read_only_fields = ("created", "sha256", "count")

class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ("created", "sha256", "count", "errors", "results")
        read_only_fields = ("created", "sha256", "count", "errors", "results")

class OutputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ("created", "sha256", "count")
        read_only_fields = ("created", "sha256", "count")       

class ContentSerializer(serializers.ModelSerializer):
    input = InputSerializer()
    output = OutputSerializer()
    class Meta:
        model = Content
        fields = ("created", "input", "output")
        read_only_fields = ("created", "input", "output")

class ContentListSerializer(serializers.ModelSerializer):
    input = InputListSerializer()
    output = OutputListSerializer()
    class Meta:
        model = Content
        fields = ("created", "input", "output")
        read_only_fields = ("created", "input", "output")

class TaskSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    content = ContentSerializer()
    runtime = RuntimeSerializer()
    class Meta:
        model = Task
        fields = ("created", "task", "status", "session", "operation", "content", "runtime")

class TaskListSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    content = ContentListSerializer()
    runtime = RuntimeListSerializer()
    class Meta:
        model = Task
        fields = ("created", "task", "status", "session", "operation", "content", "runtime")
