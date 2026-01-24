from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Asset, AssetVersion
from .serializers import AssetSerializer, AssetVersionSerializer
from erp_projects.permissions import IsProjectObjectMember, CanManageProjectObject

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectObjectMember]
    parser_classes = [MultiPartParser, FormParser]

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
        
        file = request.FILES.get('file')
        file_size = file.size if file else None
        file_type = file.content_type if file else ''
        
        # Manually construct data copy to avoid mutating QueryDict if immutable
        data = request.data.copy()
        
        serializer = AssetVersionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                asset=asset,
                version_number=next_version_number,
                file=file,
                file_size=file_size,
                file_type=file_type,
                created_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Dedicated file upload endpoint that returns file information
        """
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return file information for the frontend to use
        file_info = {
            'id': f'upload_{file.name}',
            'name': file.name,
            'size': file.size,
            'type': file.content_type,
            'url': file.url if hasattr(file, 'url') else None,
            'status': 'done'
        }
        
        return Response(file_info, status=status.HTTP_201_CREATED)

class AssetVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer
    permission_classes = [permissions.IsAuthenticated]
