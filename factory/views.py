import json
import time

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TaskSerializer, TaskListSerializer
from .models import Task

# Create your views here.

class TaskView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    ordering_fields = ['created']

    def retrieve(self, request, pk=None):
        task = Task.objects.all().filter(task_id=pk)
        if task:
            serializer = TaskSerializer(task, many=True).data[0]
            if serializer:
                serializer["content"]["results"] = json.loads(serializer["content"]["results"])
                serializer["content"]["errors"] = json.loads(serializer["content"]["errors"])
                if serializer["runtime"]["stop"] == 0:
                    serializer["runtime"]["runtime"] = time.time() - serializer["runtime"]["start"]
                return Response(serializer)
        return Response(status=404)