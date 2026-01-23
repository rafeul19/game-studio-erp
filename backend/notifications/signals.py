from django.db.models.signals import post_save
from django.dispatch import receiver
from erp_projects.models import Task
from .utils import notify_user
from activity_logs.middleware import get_current_user

@receiver(post_save, sender=Task)
def handle_task_notifications(sender, instance, created, **kwargs):
    actor = get_current_user()
    
    if created:
        # Notify assigned user
        notify_user(
            recipient=instance.assigned_to,
            verb="assigned you a task",
            actor=actor,
            target=instance
        )
    else:
        # Check if status changed
        # Note: In a real app, you'd compare current with previous state
        # For simplicity, we'll notify on every update if it's not a new task
        notify_user(
            recipient=instance.assigned_to,
            verb=f"updated task: {instance.title}",
            actor=actor,
            target=instance
        )
