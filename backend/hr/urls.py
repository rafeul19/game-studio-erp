from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, EmployeeViewSet, SkillViewSet,
    LeaveRequestViewSet, PerformanceReviewViewSet, AttendanceViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'performance-reviews', PerformanceReviewViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]