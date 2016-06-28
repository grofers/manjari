import datetime

from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import Account


class TaskViewSet(viewsets.ModelViewSet):
    '''
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        filter_argument = self.request.query_params.get('q')
        date_today = datetime.date.today()



        print request.user.id

        if filter_argument:
                filter_argument = int(filter_argument)
                date = date_today - datetime.timedelta(days=filter_argument)
                queryset = Task.objects.filter(
                    due_date__date__gte=date,user_id=request.user.id).order_by('due_date')
        if not filter_argument:
            queryset = Task.objects.filter(user_id=request.user.id).order_by('-updated_at')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user_id=Account.objects.get(email=request.user).id)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        task_id = self.get_object().id
        queryset = Tasks.objects.filter(id=task_id, user_id=request.user.id)
        if not queryset:
            return Response(status=status.HTTP_405_BAD_REQUEST)
        else:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
