from django.utils import timezone
from .models import Sprint

def automate_sprint_lifecycle():
    """
    Automatically updates sprint statuses based on the current date.
    - Dates within range: PLANNED -> ACTIVE
    - Past end_date: ACTIVE -> COMPLETED
    """
    today = timezone.now().date()
    
    # Start planned sprints
    planned_to_active = Sprint.objects.filter(
        status=Sprint.PLANNED,
        start_date__lte=today,
        end_date__gte=today
    ).update(status=Sprint.ACTIVE)
    
    # Complete active sprints
    active_to_completed = Sprint.objects.filter(
        status=Sprint.ACTIVE,
        end_date__lt=today
    ).update(status=Sprint.COMPLETED)
    
    return {
        "activated": planned_to_active,
        "completed": active_to_completed
    }
