import datetime

from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task


class TaskViewSet(viewsets.ModelViewSet):
    '''
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        filter_argument = self.request.query_params.get('q')
        date_today = datetime.date.today()

        if filter_argument:
            if filter_argument == "today":
                date = date_today.strftime("%Y-%m-%d")
                queryset = Task.objects.filter(
                    due_date__date=date).order_by('due_date')
            if filter_argument == "week":
                date = date_today - datetime.timedelta(days=7)
                queryset = Task.objects.filter(
                    due_date__date__gte=date).order_by('due_date')

        if not filter_argument:
            queryset = Task.objects.all().order_by('due_date')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
