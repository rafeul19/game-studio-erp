from django.db import models
from accounts.models import User

class RoleAction(models.Model):
    """
    Enterprise-grade Role -> Action matrix.
    Defines which roles can perform which actions globally.
    """
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    action = models.CharField(max_length=100) # e.g., 'create_project', 'delete_task'
    is_allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'action')

    def __str__(self):
        return f"{self.role} -> {self.action} ({'Allowed' if self.is_allowed else 'Denied'})"

class ProjectRoleOverride(models.Model):
    """
    Allows overriding global role permissions for a specific project.
    """
    project = models.ForeignKey('erp_projects.Project', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_override = models.CharField(max_length=20, choices=User.ROLE_CHOICES)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.project.name} as {self.role_override}"
