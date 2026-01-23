from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .permissions import IsAdmin, IsAdminOrManager


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "OK",
        "service": "ERP Backend",
        "auth": "JWT ready"
    })

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    })

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard(request):
    return Response({
        "message": "Admin dashboard access granted"
    })


@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def management_dashboard(request):
    return Response({
        "message": "Manager / Admin access granted"
    })

