from django.db.models.signals import post_save
from django.dispatch import receiver
from erp_projects.models import Task
from .utils import notify_user
from activity_logs.middleware import get_current_user

from bugs.models import Bug
from assets.models import AssetVersion

@receiver(post_save, sender=Task)
def handle_task_notifications(sender, instance, created, **kwargs):
    actor = get_current_user()
    
    if created:
        notify_user(
            recipient=instance.assigned_to,
            verb="assigned you a task",
            actor=actor,
            target=instance
        )

@receiver(post_save, sender=Bug)
def handle_bug_notifications(sender, instance, created, **kwargs):
    actor = get_current_user()
    if created and instance.assignee:
        notify_user(
            recipient=instance.assignee,
            verb="assigned you a bug",
            actor=actor,
            target=instance
        )

@receiver(post_save, sender=AssetVersion)
def handle_asset_version_notifications(sender, instance, created, **kwargs):
    if created:
        project = instance.asset.project
        members = project.members.all()
        actor = instance.uploaded_by
        for member in members:
            if member != actor:
                notify_user(
                    recipient=member,
                    verb=f"uploaded a new version of asset: {instance.asset.name}",
                    actor=actor,
                    target=instance.asset
                )
