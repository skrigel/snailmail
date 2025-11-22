from django.contrib import admin
from .models import DailyStat

@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'inbox_count', 'sent_count', 'work', 'personal', 'promotions')
    list_filter = ('date',)
    date_hierarchy = 'date'
    search_fields = ('owner__username', 'owner__email')
    list_select_related = ('owner',)
    ordering = ('-date',)
