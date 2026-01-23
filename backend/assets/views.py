from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Asset, AssetVersion
from .serializers import AssetSerializer, AssetVersionSerializer
from erp_projects.permissions import IsProjectObjectMember, CanManageProjectObject

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectObjectMember]

    def get_permissions(self):
        if self.action in ['destroy', 'add_version']:
            return [permissions.IsAuthenticated(), CanManageProjectObject()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_version(self, request, pk=None):
        asset = self.get_object()
        latest_version = asset.get_latest_version()
        next_version_number = (latest_version.version_number + 1) if latest_version else 1
        
        serializer = AssetVersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                asset=asset,
                version_number=next_version_number,
                created_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer
    permission_classes = [permissions.IsAuthenticated]
