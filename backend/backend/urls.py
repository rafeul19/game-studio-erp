from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    admin_dashboard,
    management_dashboard,
    health_check,
    profile_view,
    dashboard_stats,
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
    suggest_task_story_points,
    predict_sprint_risk,
    detect_asset_reuse_api,
    sprint_capacity_planning_api,
    log_work,
    transfer_project_ownership,
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
    path('api/dashboard/stats/', dashboard_stats),

    # Projects
    path('api/projects/create/', create_project),
    path('api/projects/my/', my_projects),
    path('api/projects/<int:project_id>/progress/', project_progress),
    path('api/projects/<int:project_id>/sprints/', project_sprints),
    path('api/projects/<int:project_id>/transfer/', transfer_project_ownership),

    # Tasks
    path('api/tasks/create/', create_task),
    path('api/tasks/my/', my_tasks),
    path('api/tasks/<int:task_id>/status/', update_task_status),
    path('api/tasks/overdue/', overdue_tasks),
    path('api/tasks/suggest-points/', suggest_task_story_points),
    path('api/tasks/asset-reuse/', detect_asset_reuse_api),
    path('api/tasks/log-work/', log_work),

    # Sprints
    path('api/sprints/create/', create_sprint),
    path('api/sprints/<int:sprint_id>/progress/', sprint_progress),
    path('api/sprints/<int:sprint_id>/risk/', predict_sprint_risk),
    path('api/projects/<int:project_id>/suggested-capacity/', sprint_capacity_planning_api),

    # Reports
    path('api/reports/productivity/', productivity_report),

    # Audit
    path('', include('activity_logs.urls')),

    # Notifications
    path('', include('notifications.urls')),
    
    # Core Modules (Phase 2)
    path('api/', include('assets.urls')),
    path('api/', include('bugs.urls')),
    path('api/hr/', include('hr.urls')),
    path('api/', include('finance.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
