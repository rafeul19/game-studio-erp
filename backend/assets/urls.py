from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, AssetVersionViewSet

router = DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'versions', AssetVersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
