from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import (
    admin_dashboard,
    management_dashboard,
    health_check,
    profile_view,
)

from erp_projects.views import (
    create_project,
    my_projects,
    project_progress,
    create_task,
    my_tasks,
    update_task_status,
    overdue_tasks,
    create_sprint,
    sprint_progress,
    project_sprints,
    productivity_report,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health
    path('api/health/', health_check),

    # Auth
    path('api/profile/', profile_view),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # Dashboards
    path('api/admin/dashboard/', admin_dashboard),
    path('api/management/dashboard/', management_dashboard),

    # Projects
    path('api/projects/create/', create_project),
    path('api/projects/my/', my_projects),
    path('api/projects/<int:project_id>/progress/', project_progress),
    path('api/projects/<int:project_id>/sprints/', project_sprints),

    # Tasks
    path('api/tasks/create/', create_task),
    path('api/tasks/my/', my_tasks),
    path('api/tasks/<int:task_id>/status/', update_task_status),
    path('api/tasks/overdue/', overdue_tasks),

    # Sprints
    path('api/sprints/create/', create_sprint),
    path('api/sprints/<int:sprint_id>/progress/', sprint_progress),

    # Reports
    path('api/reports/productivity/', productivity_report),
]
