from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DailyStat
from .serializers import DailyStatSerializer


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
