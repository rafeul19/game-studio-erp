from rest_framework.permissions import BasePermission
from accounts.models import User


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [User.ADMIN, User.MANAGER]
        )


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.owner or
            request.user in obj.members.all()
        )

class CanCreateTask(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [User.ADMIN, User.MANAGER]
        )

class CanManageSprint(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [User.ADMIN, User.MANAGER]
        )

class CanUpdateTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin / Manager can update any task
        if request.user.role in [User.ADMIN, User.MANAGER]:
            return True

        # Others can update ONLY their own tasks
        return obj.assigned_to == request.user

