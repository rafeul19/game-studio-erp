from rest_framework import serializers
from .models import Project, Sprint, Task
from accounts.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'created_at', 'progress_percentage']
        read_only_fields = ['owner', 'created_at']

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'name', 'project', 'start_date', 'end_date', 'status', 'created_at', 'progress_percentage']
        read_only_fields = ['created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'status', 'due_date', 'sprint', 'created_at']
        read_only_fields = ['created_at']
