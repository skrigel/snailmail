from django.contrib import admin
from .models import GoogleUser

@admin.register(GoogleUser)
class GoogleUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'google_id', 'user')
    search_fields = ('username', 'email', 'google_id', 'user__username')
    list_select_related = ('user',)
