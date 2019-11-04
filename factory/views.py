import json
import time

from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TaskSerializer, TaskListSerializer, SessionListSerializer, TaskSummarySerializer
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
        task = Task.objects.filter(task=pk).first()
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        return Response(status=404)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        task = Task.objects.filter(task=pk).first()
        if task:
            serializer = TaskSummarySerializer(task)
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
        session = Session.objects.filter(Q(name=pk) | Q(session_id=pk)).first()
        if session:
            serializer = SessionListSerializer(session)
            return Response(serializer.data)
        return Response(status=404)