"""
URL configuration for snailmail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.http import HttpResponseRedirect
from authentication.views import (
    csrf,
    auth_status,
    google_login_redirect,
    google_callback,
    logout_view
)

def to_spa_app(_request):
    # In dev, send users to the Next.js app
    return HttpResponseRedirect("http://localhost:3000/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    # JSON auth helpers (must come BEFORE any catch-all)
    path("api/auth/csrf/", csrf, name="csrf"),
    path("api/auth/status/", auth_status, name="auth-status"),
    path("api/auth/google/login/", google_login_redirect, name="google-login"),
    path("api/auth/google/callback/", google_callback, name="google-callback"),
    path("api/auth/logout/", logout_view, name="logout"),

    # API endpoints
    path("api/mail/", include("mail.urls")),
    path("api/analytics/", include("analytics.urls")),

    # Optional: if you also want /app on Django to bounce to the SPA
    path("app", to_spa_app, name="app-redirect"),

    # Catch-all ONLY for front-end client routing — exclude API/admin/accounts/static/media
    re_path(r"^(?!api/|accounts/|admin/|static/|media/).*$", to_spa_app),
]