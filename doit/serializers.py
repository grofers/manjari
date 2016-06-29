from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model = Task
        fields = ('id','description', 'due_date', 'task_status')
