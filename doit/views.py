import datetime

from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import Account


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000


class TaskViewSet(viewsets.ModelViewSet):
    '''
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    pagination_class = StandardResultsSetPagination
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        filter_argument = self.request.query_params.get('q')
        date_today = datetime.date.today()
        response = {}
        status = {}
        data = {}

        if filter_argument:
                filter_argument = int(filter_argument)
                date = date_today - datetime.timedelta(days=filter_argument)
                queryset = Task.objects.filter(
                    due_date__date__gte=date,
                    user_id=request.user.id).order_by('due_date')
        if not filter_argument:
            queryset = Task.objects.filter(
                user_id=request.user.id).order_by('-updated_at')
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            status['success'] = True
            data['tasks'] = serializer.data
            response['status'] = status
            response['data'] = data
            return Response(response)

        status['success'] = False
        error = {}
        error['msg'] = 'Invalid Page'
        status['error'] = error
        response['status'] = status
        return Response(response, status=404)

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
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
