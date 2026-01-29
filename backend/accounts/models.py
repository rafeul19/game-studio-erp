from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for ERP system
    """

    # ✅ ROLE CONSTANTS (single source of truth)
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    DEVELOPER = 'DEVELOPER'
    ARTIST = 'ARTIST'
    QA = 'QA'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
        (ARTIST, 'Artist'),
        (QA, 'QA'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=DEVELOPER
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

from .permissions_models import RoleAction, ProjectRoleOverride
