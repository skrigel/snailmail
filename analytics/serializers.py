from rest_framework import serializers
from .models import DailyStat


class DailyStatSerializer(serializers.ModelSerializer):
    """Serializer for daily email statistics"""

    class Meta:
        model = DailyStat
        fields = [
            'id',
            'date',
            'inbox_count',
            'sent_count',
            'work',
            'personal',
            'promotions',
        ]
        read_only_fields = ['id', 'owner']