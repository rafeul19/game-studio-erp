from rest_framework import serializers
from .models import ActivityLog
from accounts.serializers import UserSerializer

class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'action', 'content_type_name', 
            'object_id', 'description', 'changes', 'timestamp'
        ]
