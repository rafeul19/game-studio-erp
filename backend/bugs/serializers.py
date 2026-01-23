from rest_framework import serializers
from .models import Bug

class BugSerializer(serializers.ModelSerializer):
    reporter_name = serializers.ReadOnlyField(source='reporter.username')
    assignee_name = serializers.ReadOnlyField(source='assignee.username')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Bug
        fields = [
            'id', 'title', 'description', 'severity', 'status', 
            'project', 'project_name', 'reporter', 'reporter_name',
            'assignee', 'assignee_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reporter', 'created_at', 'updated_at']
