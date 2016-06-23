from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from .serializers import TaskSerializer
from .models import Task


class TaskViewSet(viewsets.ModelViewSet):
    '''
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
