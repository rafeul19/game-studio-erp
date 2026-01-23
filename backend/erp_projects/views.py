from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Project, Task, Sprint
from .serializers import ProjectSerializer, TaskSerializer, SprintSerializer
from .permissions import IsAdminOrManager, IsProjectMember, CanCreateTask, CanManageSprint, CanUpdateTask
from .utils import is_valid_status_transition

# --- Projects ---

@api_view(['POST'])
@permission_classes([IsAdminOrManager])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_projects(request):
    projects = Project.objects.filter(members=request.user) | Project.objects.filter(owner=request.user)
    serializer = ProjectSerializer(projects.distinct(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_progress(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return Response({
        "project": project.name,
        "progress": project.progress_percentage()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_sprints(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    sprints = project.sprints.all()
    serializer = SprintSerializer(sprints, many=True)
    return Response(serializer.data)

# --- Tasks ---

@api_view(['POST'])
@permission_classes([CanCreateTask])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        # Default assigned_to to the creator if not provided
        if not serializer.validated_data.get('assigned_to'):
            serializer.save(assigned_to=request.user)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check object permission manually for function view if needed, 
    # but CanUpdateTask has_object_permission should be handled by DRF if using generic views.
    # For function views, we must call it.
    perm = CanUpdateTask()
    if not perm.has_object_permission(request, None, task):
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    new_status = request.data.get('status')
    if not is_valid_status_transition(task.status, new_status):
        return Response({"error": f"Invalid transition from {task.status} to {new_status}"}, status=status.HTTP_400_BAD_REQUEST)
    
    task.status = new_status
    task.save()
    return Response(TaskSerializer(task).data)

@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def overdue_tasks(request):
    tasks = Task.objects.filter(due_date__lt=timezone.now().date()).exclude(status='DONE')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

# --- Sprints ---

@api_view(['POST'])
@permission_classes([CanManageSprint])
def create_sprint(request):
    serializer = SprintSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sprint_progress(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    return Response({
        "sprint": sprint.name,
        "progress": sprint.progress_percentage()
    })

# --- Reports ---

@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def productivity_report(request):
    # Basic logic: count tasks completed by each user
    from accounts.models import User
    users = User.objects.all()
    report = []
    for user in users:
        total = user.tasks.count()
        done = user.tasks.filter(status='DONE').count()
        total_points = sum(t.story_points for t in user.tasks.all())
        done_points = sum(t.story_points for t in user.tasks.filter(status='DONE'))
        
        report.append({
            "username": user.username,
            "total_tasks": total,
            "completed_tasks": done,
            "total_story_points": total_points,
            "completed_story_points": done_points,
            "productivity_score": int((done_points / total_points * 100)) if total_points > 0 else 0
        })
    return Response(report)

# --- AI Features ---

@api_view(['POST'])
@permission_classes([IsAdminOrManager])
def suggest_task_story_points(request):
    title = request.data.get('title', '')
    description = request.data.get('description', '')
    from .ai_service import AIEstimationService
    points = AIEstimationService.suggest_story_points(title, description)
    return Response({"suggested_points": points})

@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def predict_sprint_risk(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    from .ai_service import AIEstimationService
    risk = AIEstimationService.predict_sprint_risk(sprint)
    return Response({
        "sprint": sprint.name,
        "risk_level": risk
    })

@api_view(['POST'])
@permission_classes([IsAdminOrManager])
def detect_asset_reuse_api(request):
    project_id = request.data.get('project_id')
    project = get_object_or_404(Project, id=project_id)
    task_title = request.data.get('title', '')
    from .ai_service import AIEstimationService
    matches = AIEstimationService.detect_asset_reuse(project, task_title)
    return Response({"potential_reuse": matches})

@api_view(['GET'])
@permission_classes([IsAdminOrManager])
def sprint_capacity_planning_api(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    from .ai_service import AIEstimationService
    capacity = AIEstimationService.calculate_sprint_capacity(project)
    return Response({
        "project": project.name,
        "suggested_sprint_capacity": capacity
    })

# --- Time & Ownership ---

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_work(request):
    serializer = WorkLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_project_ownership(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user and request.user.role != User.ADMIN:
        return Response({"error": "Only project owner or admin can transfer ownership"}, status=status.HTTP_403_FORBIDDEN)
    
    new_owner_id = request.data.get('new_owner_id')
    new_owner = get_object_or_404(User, id=new_owner_id)
    
    project.owner = new_owner
    project.save()
    return Response({"message": f"Ownership transferred to {new_owner.username}"})
