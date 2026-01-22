from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    target_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 
            'target_type', 'object_id', 'is_read', 'created_at'
        ]
