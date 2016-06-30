import datetime

from django.conf import settings
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.models import Account


def home(request):
    return render(request, 'main.html', {'STATIC_URL': settings.STATIC_URL})


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000


class TaskViewSet(viewsets.ModelViewSet):
    '''
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
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
                date = date_today + datetime.timedelta(days=filter_argument)
                queryset = Task.objects.filter(
                    active_flag=True,
                    user_id=request.user.id,
                    due_date__date__gte=date_today,
                    due_date__date__lte=date).order_by('-due_date')
        if not filter_argument:
            queryset = Task.objects.filter(
                active_flag=True,
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
        response = {}
        status = {}
        data = {}
        task_id = self.get_object().id
        queryset = Task.objects.filter(id=task_id, user_id=request.user.id)
        if not queryset:
            status['success'] = False
            error = {}
            error['msg'] = 'Delete not Authorized'
            status['error'] = error
            response['status'] = status
            return Response(response, status=403)
        else:
            instance = self.get_object()
            instance.active_flag = False
            instance.save()
            status['success'] = True
            response['status'] = status
            return Response(response, status=204)

    def retrieve(self, request, *args, **kwargs):
        response = {}
        status = {}
        data = {}
        task_id = self.get_object().id
        queryset = Task.objects.filter(
            id=task_id, user_id=request.user.id,
            active_flag=True)
        if not queryset:
            status['success'] = False
            error = {}
            error['msg'] = 'Invalid TaskId'
            status['error'] = error
            response['status'] = status
            return Response(response, status=403)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            status['success'] = True
            data['tasks'] = serializer.data
            response['status'] = status
            response['data'] = data
            return Response(response)

    def update(self, request, *args, **kwargs):
        response = {}
        status = {}
        data = {}
        task_id = self.get_object().id
        queryset = Task.objects.filter(
            id=task_id, user_id=request.user.id,
            active_flag=True)
        if not queryset:
            status['success'] = False
            error = {}
            error['msg'] = 'Invalid TaskId'
            status['error'] = error
            response['status'] = status
            return Response(response, status=403)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            status['success'] = True
            data['tasks'] = serializer.data
            response['status'] = status
            response['data'] = data
            return Response(response)
