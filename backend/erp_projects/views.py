from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from .permissions import IsAdminOrManager
from .models import Task
from .permissions import CanCreateTask, CanUpdateTask



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def create_project(request):
    project = Project.objects.create(
        name=request.data.get('name'),
        description=request.data.get('description', ''),
        owner=request.user
    )
    project.members.add(request.user)
    return Response({"message": "Project created successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_projects(request):
    projects = Project.objects.filter(members=request.user)
    return Response([
        {"id": p.id, "name": p.name} for p in projects
    ])

@api_view(['POST'])
@permission_classes([IsAuthenticated, CanCreateTask])
def create_task(request):
    task = Task.objects.create(
        title=request.data.get('title'),
        description=request.data.get('description', ''),
        project_id=request.data.get('project_id'),
        assigned_to_id=request.data.get('assigned_to'),
    )
    return Response({"message": "Task created successfully"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return Response([
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "project": t.project.name
        }
        for t in tasks
    ])

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, CanUpdateTask])
def update_task_status(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = request.data.get('status')
    task.save()
    return Response({"message": "Task status updated"})

