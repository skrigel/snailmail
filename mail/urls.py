from django.urls import path
from . import views

app_name = "mail"
urlpatterns = [
    path("summary/", views.snail_summary, name="snail-summary"),
    path("sync/", views.trigger_gmail_sync, name="trigger-sync"),
]
