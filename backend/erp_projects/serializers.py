from rest_framework import serializers
from .models import Project, Sprint, Task, WorkLog
from accounts.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'budget_type', 'total_budget', 'created_at', 'progress_percentage']
        read_only_fields = ['owner', 'created_at', 'progress_percentage']

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'name', 'project', 'start_date', 'end_date', 'status', 'created_at', 'progress_percentage']
        read_only_fields = ['created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'status', 'priority', 'due_date', 'sprint', 'story_points', 'created_at']
        read_only_fields = ['created_at']

class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = ['id', 'task', 'user', 'hours', 'description', 'is_billable', 'timestamp']
        read_only_fields = ['user', 'timestamp']
