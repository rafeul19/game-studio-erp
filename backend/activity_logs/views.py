from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from erp_projects.permissions import IsAdminOrManager

@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def audit_dashboard(request):
    """
    View to list all activity logs for admins and managers.
    """
    logs = ActivityLog.objects.all()[:100]  # Limit to latest 100 logs
    serializer = ActivityLogSerializer(logs, many=True)
    return Response(serializer.data)
