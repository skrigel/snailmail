from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DailyStat
from .serializers import DailyStatSerializer
from .tasks import calculate_daily_stats


class DailyStatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for daily email statistics.
    Users can only see their own stats.
    """
    serializer_class = DailyStatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return stats for the current user
        return DailyStat.objects.filter(owner=self.request.user).order_by('-date')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_stats_calculation(request):
    """
    API endpoint to trigger daily stats calculation.
    """
    days = request.data.get('days', 30)

    # Queue the Celery task
    task = calculate_daily_stats.delay(request.user.id, days=days)

    return Response({
        "success": True,
        "message": f"Stats calculation queued for last {days} days",
        "task_id": task.id
    })

