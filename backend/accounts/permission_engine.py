from .models import RoleAction, ProjectRoleOverride

class DynamicPermissionEngine:
    @staticmethod
    def has_permission(user, action, project=None):
        """
        Main entry point for checking permissions.
        1. Check if user has a project-level role override.
        2. Check the RoleAction matrix for that role (or global role).
        """
        role = user.role
        
        # 1. Project-level override
        if project:
            override = ProjectRoleOverride.objects.filter(project=project, user=user).first()
            if override:
                role = override.role_override
        
        # 2. Check RoleAction matrix
        # If no entry exists, we can decide on default (allow or deny)
        # For security, let's deny by default if entry exists but is_allowed=False, 
        # or allow if no specific restriction exists for that role/action.
        permission = RoleAction.objects.filter(role=role, action=action).first()
        if permission:
            return permission.is_allowed
        
        # Default policy: Manager/Admin allowed for most things, Developer restricted.
        # This is a fallback if the matrix isn't fully populated.
        if role in ['admin', 'manager']:
            return True
        return False
