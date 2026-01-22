from django.db import models
from accounts.models import User
from erp_projects.models import Project

class Bug(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('TRIAGE', 'Triage'),
        ('IN_PROGRESS', 'In Progress'),
        ('BLOCKED', 'Blocked'),
        ('RESOLVED', 'Resolved'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TRIAGE')
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='bugs'
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_bugs'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_bugs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-severity', '-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.title}"
