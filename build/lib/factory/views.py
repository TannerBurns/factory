import json
import time

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TaskSerializer, TaskListSerializer, SessionListSerializer
from .models import Task, Session

# Create your views here.

class TaskView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    ordering_fields = ['created']

    
    def retrieve(self, request, pk=None):
        """retrieve
        
        Arguments:
            request -- incoming request object
        
        Keyword Arguments:
            pk {str} -- task id to match (default: {None})
        
        Returns:
            Response -- response contains the data and status code
        """
        task = Task.objects.all().filter(task=pk)
        if task:
            serializer = TaskSerializer(task, many=True)
            
            # updating serialized data
            # iterate over serialized data to convert str to json from the database
            # add current runtime to serialized data
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
            # attempt to return only the first task found
            try:
                return Response(serializer.data[0])
            except Exception:
                return Response(serializer.data)
        return Response(status=404)
    
class SessionView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Session.objects.all()
    serializer_class = SessionListSerializer
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['created']

    def retrieve(self, request, pk=None):
        """retrieve
        
        Arguments:
            request -- incoming request object
        
        Keyword Arguments:
            pk {str} -- session id to match (default: {None})
        
        Returns:
            Response -- response contains the data and status code
        """
        print(pk)
        session = Session.objects.all().filter(Q(name=pk) | Q(session_id=pk))
        if session:
            serializer = SessionListSerializer(session, many=True)
            return Response(serializer.data)
        return Response(status=404)