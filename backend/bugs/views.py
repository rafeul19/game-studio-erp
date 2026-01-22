from rest_framework import viewsets, permissions
from .models import Bug
from .serializers import BugSerializer
from erp_projects.permissions import IsProjectObjectMember, CanUpdateBug, CanManageProjectObject

class BugViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectObjectMember]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), CanUpdateBug()]
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), CanManageProjectObject()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
