from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET

@ensure_csrf_cookie
@require_GET
def csrf(request):
    return JsonResponse({"ok": True})

@require_GET
def auth_status(request):
    if request.user.is_authenticated:
        u = request.user
        return JsonResponse({
            "authenticated": True,
            "user": {"id": u.id, "username": u.username, "email": u.email}
        })
    return JsonResponse({"authenticated": False})