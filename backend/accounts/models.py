from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for ERP system
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('artist', 'Artist'),
        ('qa', 'QA'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='developer'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
