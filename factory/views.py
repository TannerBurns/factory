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
    filterset_fields = ['status', 'session']
    ordering_fields = ['created']

    
    def retrieve(self, request, pk=None):
        task = Task.objects.all().filter(task=pk)
        if task:
            serializer = TaskSerializer(task, many=True)
            
            for i in range(0, len(serializer.data)):
                if serializer.data[i]:
                    serializer.data[i] = dict(serializer.data[i])
                    serializer.data[i]["content"][0]["results"] = json.loads(
                        serializer.data[i]["content"][0]["results"]
                    )
                    serializer.data[i]["content"][0]["errors"] = json.loads(
                        serializer.data[i]["content"][0]["errors"]
                    )
                    if serializer.data[i]["runtime"]["stop"] == 0:
                        serializer.data[i]["runtime"]["total"] = time.time() - serializer.data[i]["runtime"]["start"]
            return Response(serializer.data)
        return Response(status=404)
    
