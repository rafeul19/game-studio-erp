from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .permissions import IsAdmin, IsAdminOrManager


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "OK",
        "service": "ERP Backend",
        "auth": "JWT ready"
    })

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    })

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard(request):
    return Response({
        "message": "Admin dashboard access granted"
    })


@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def management_dashboard(request):
    return Response({
        "message": "Manager / Admin access granted"
    })

from erp_projects.models import Project, Task, Sprint
from bugs.models import Bug

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    # Base querysets
    user = request.user
    # Admin sees all, others see their own or public data? 
    # For now, let's show studio-wide stats for impact, 
    # but in a real app might filter by request.user.
    
    # 1. Active Projects Count
    # Assuming 'active' means not deleted or archived. 
    # We can check if status is not 'COMPLETED' if that field existed, 
    # but based on models it has progress.
    active_projects_count = Project.objects.count() 
    
    # 2. Tasks stats
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='DONE').count()
    
    # 3. Bugs
    open_bugs = Bug.objects.exclude(status='RESOLVED').count()
    
    # 4. Project status distribution (Simulated based on progress)
    # We'll return the raw projects for the table
    # Optimize: limit to recent 5
    recent_projects = Project.objects.all().order_by('-created_at')[:5]
    project_data = []
    for p in recent_projects:
        # Determine strict status based on progress
        progress = p.progress_percentage()
        status = 'In Progress'
        if progress == 100:
            status = 'Completed'
        elif progress < 20: 
            status = 'At Risk' # Arbitrary logic for demo
            
        project_data.append({
            'id': p.id,
            'name': p.name,
            'status': status,
            'progress': progress
        })

    # 5. Sprint Velocities (Last 5 sprints)
    # Get completed sprints
    recent_sprints = Sprint.objects.filter(status='COMPLETED').order_by('-end_date')[:5]
    # If no completed sprints, maybe show active ones?
    # Let's mix them for the chart
    mixed_sprints = Sprint.objects.all().order_by('created_at')[:5]
    
    sprint_data = []
    for s in mixed_sprints:
        velocity = s.velocity() if s.status == 'COMPLETED' else s.total_story_points()
        bugs_count = 0 # Need to link bugs to sprints if possible? 
        # Bug model doesn't link to Sprint directly, only Project.
        # We can approximate by date or just mock it relative to severity for now
        # OR count bugs created during sprint timeframe? 
        # Let's keep it simple: 
        bugs_count = Bug.objects.filter(project=s.project, created_at__range=[s.start_date, s.end_date]).count()
        
        sprint_data.append({
            'name': s.name,
            'velocity': velocity,
            'bugs': bugs_count
        })

    return Response({
        "active_projects": active_projects_count,
        "completed_tasks": completed_tasks,
        "pending_approval": 0, # Placeholder if no specific 'Approval' logic
        "open_bugs": open_bugs,
        "sprint_data": sprint_data,
        "project_data": project_data,
    })

