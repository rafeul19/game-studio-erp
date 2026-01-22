from django.urls import path
from .views import my_notifications, mark_as_read

urlpatterns = [
    path('api/notifications/', my_notifications, name='my-notifications'),
    path('api/notifications/<int:notification_id>/read/', mark_as_read, name='mark-notification-read'),
]
