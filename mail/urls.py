from django.urls import path
from . import views

app_name = "mail"
urlpatterns = [
    path("api/snails/summary/", views.snail_summary, name="snail-summary"),
]
