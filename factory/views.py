import json
import time

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TasksSerializer, TaskSerializer
from .models import Tasks

# Create your views here.

class TasksView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['session']
    ordering_fields = ['created']

    def retrieve(self, request, pk=None):
        task = Tasks.objects.all().filter(task_id=pk)
        if task:
            serializer = TaskSerializer(task, many=True).data[0]
            if serializer:
                serializer["results"] = json.loads(serializer["results"])
                if task.get().runtime == 0:
                    serializer["runtime"] = time.time() - task.get().start
                else:
                    serializer["runtime"] = task.get().runtime
                return Response(serializer)
        return Response(status=404)