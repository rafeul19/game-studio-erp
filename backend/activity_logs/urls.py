from django.urls import path
from .views import audit_dashboard

urlpatterns = [
    path('api/audit/', audit_dashboard, name='audit-dashboard'),
]
