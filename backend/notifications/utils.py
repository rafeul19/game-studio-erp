from .models import Notification
from django.core.mail import send_mail
from django.conf import settings

def notify_user(recipient, verb, actor=None, target=None):
    """
    Creates an in-app notification and sends an email.
    """
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target
    )
    
    # Placeholder for email notification
    subject = f"ERP Notification: {verb}"
    message = f"Hello {recipient.username},\n\n{actor} {verb}."
    if target:
        message += f" (Target: {target})"
    
    # In a real app, you'd use Celery here
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient.email], fail_silently=True)
    
    return notification
