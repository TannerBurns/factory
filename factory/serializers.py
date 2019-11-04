from rest_framework import serializers

from .models import Task, Operation, Runtime, Content, Session


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('created', 'sha256', 'name', 'docstring')
        read_only_fields = ('created', 'sha256', 'name', 'docstring')


class RuntimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ('created', 'start', 'stop', 'total')
        read_only_fields = ('created', 'start', 'stop', 'total')


class RuntimeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ('created', 'start',)
        read_only_fields = ('created', 'start',) 


class ContentSerializer(serializers.ModelSerializer):
    errors = serializers.ListField()
    results = serializers.ListField()
    class Meta:
        model = Content
        fields = ('created', 'errors', 'results')
        read_only_fields = ('created', 'errors', 'results')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('created', 'name', 'session_id')
        read_only_fields = ('created', 'name', 'session_id') 


class TaskSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    sessions = SessionSerializer(many=True)
    content = ContentSerializer(many=True)
    runtime = RuntimeSerializer()
    class Meta:
        model = Task
        fields = ('created', 'task', 'status', 'sessions', 'operation', 'content', 'runtime')
        read_only_fields = ('created', 'task', 'status', 'sessions', 'operation', 'content', 'runtime')

class TaskSummarySerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    runtime = RuntimeSerializer()
    class Meta:
        model = Task
        fields = ('created', 'task', 'status', 'operation', 'runtime')
        read_only_fields = ('created', 'task', 'status', 'operation', 'runtime')

class TaskSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('created', 'task', 'status', )
        read_only_fields = ('created', 'task', 'status', )


class SessionListSerializer(serializers.ModelSerializer):
    tasks = TaskSessionSerializer(many=True)
    class Meta:
        model = Session
        fields = ('created', 'name', 'session_id', 'tasks')
        read_only_fields = ('created', 'start', 'session_id', 'tasks') 


class TaskListSerializer(serializers.ModelSerializer):
    operation = OperationSerializer()
    sessions = SessionSerializer(many=True)
    runtime = RuntimeListSerializer()
    class Meta:
        model = Task
        fields = ('created', 'task', 'status', 'sessions', 'operation', 'runtime')
        read_only_fields = ('created', 'task', 'status', 'sessions', 'operation', 'runtime')
