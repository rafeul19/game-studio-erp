from rest_framework.permissions import BasePermission
from accounts.models import User
from .models import Project


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role in [User.ADMIN, User.MANAGER] or request.user.is_superuser)
        )


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser or
            request.user == obj.owner or
            request.user in obj.members.all()
        )

class CanCreateTask(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role in [User.ADMIN, User.MANAGER, User.DEVELOPER] or request.user.is_superuser)
        )

class CanManageSprint(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role in [User.ADMIN, User.MANAGER] or request.user.is_superuser)
        )

class CanUpdateTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin / Manager / Superuser can update any task
        if request.user.is_superuser or request.user.role in [User.ADMIN, User.MANAGER]:
            return True

        # Others can update ONLY their own tasks
        return obj.assigned_to == request.user

class IsProjectObjectMember(BasePermission):
    """
    Check if user is a member of the project associated with the object.
    Object must have a 'project' attribute or be a Project itself.
    """
    def has_object_permission(self, request, view, obj):
        project = obj if isinstance(obj, Project) else getattr(obj, 'project', None)
        if not project:
            return False
        return (
            request.user.is_superuser or
            request.user == project.owner or
            request.user in project.members.all()
        )

class CanManageProjectObject(BasePermission):
    """
    Only admin, manager, or project owner can perform destructive or management actions.
    """
    def has_object_permission(self, request, view, obj):
        project = obj if isinstance(obj, Project) else getattr(obj, 'project', None)
        if not project:
            return False
        return (
            request.user.is_superuser or
            request.user.role in [User.ADMIN, User.MANAGER] or
            request.user == project.owner
        )

class CanUpdateBug(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin / Manager / Superuser can update any bug
        if request.user.is_superuser or request.user.role in [User.ADMIN, User.MANAGER]:
            return True
        # Assigned user or reporter can update
        return obj.assignee == request.user or obj.reporter == request.user
