from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyStatViewSet

router = DefaultRouter()
router.register(r'daily-stats', DailyStatViewSet, basename='dailystat')

urlpatterns = [
    path('', include(router.urls)),
]