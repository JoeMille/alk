from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, ThreadViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'threads', ThreadViewSet, basename='thread')

urlpatterns = [
    path('', include(router.urls)),
]