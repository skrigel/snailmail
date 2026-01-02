from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyStatViewSet, trigger_stats_calculation

router = DefaultRouter()
router.register(r'daily-stats', DailyStatViewSet, basename='dailystat')

urlpatterns = [
    path('', include(router.urls)),
          path('calculate/', trigger_stats_calculation, name='calculate-stats'),

]