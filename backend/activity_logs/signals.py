from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog
from .middleware import get_current_user
from erp_projects.models import Project, Sprint, Task
from assets.models import Asset, AssetVersion
from bugs.models import Bug

def log_action(instance, action, description, changes=None):
    user = get_current_user()
    content_type = ContentType.objects.get_for_model(instance)
    ActivityLog.objects.create(
        user=user,
        action=action,
        content_type=content_type,
        object_id=instance.id,
        description=description,
        changes=changes
    )

@receiver(post_save, sender=Project)
@receiver(post_save, sender=Sprint)
@receiver(post_save, sender=Task)
@receiver(post_save, sender=Asset)
@receiver(post_save, sender=AssetVersion)
@receiver(post_save, sender=Bug)
def handle_post_save(sender, instance, created, **kwargs):
    action = ActivityLog.CREATED if created else ActivityLog.UPDATED
    desc_prefix = "Created" if created else "Updated"
    description = f"{desc_prefix} {sender.__name__}: {instance}"
    
    # Simple change tracking can be added here if needed
    # For now, just logging the action
    log_action(instance, action, description)

@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Sprint)
@receiver(post_delete, sender=Task)
@receiver(post_delete, sender=Asset)
@receiver(post_delete, sender=Bug)
def handle_post_delete(sender, instance, **kwargs):
    description = f"Deleted {sender.__name__}: {instance}"
    log_action(instance, ActivityLog.DELETED, description)
