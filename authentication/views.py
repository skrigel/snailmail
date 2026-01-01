from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import login as django_login, logout as django_logout
from django.urls import reverse
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import os
import requests
import json


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


def google_login_redirect(request):
    """
    Initiates Google OAuth flow by redirecting to Google's authorization URL
    """
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    redirect_uri = "http://localhost:3000/auth/callback/google"

    if not client_id:
        return JsonResponse(
            {"error": "Google OAuth not configured"},
            status=500
        )

    scope = "openid email profile"
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&access_type=offline"
        f"&prompt=consent"
    )

    return redirect(auth_url)


@csrf_exempt
@require_POST
def google_callback(request):
    """
    Handles the callback from Google OAuth with the authorization code
    """
    from django.contrib.auth.models import User
    from allauth.socialaccount.models import SocialAccount

    try:
        data = json.loads(request.body)
        code = data.get('code')

        if not code:
            return JsonResponse(
                {"error": "No authorization code provided"},
                status=400
            )

        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        redirect_uri = "http://localhost:3000/auth/callback/google"

        # Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        if 'error' in token_json:
            return JsonResponse(
                {"error": token_json['error']},
                status=400
            )

        access_token = token_json.get('access_token')

        # Get user info from Google
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo = userinfo_response.json()

        email = userinfo.get('email')
        google_id = userinfo.get('id')
        name = userinfo.get('name', '')
        given_name = userinfo.get('given_name', '')
        family_name = userinfo.get('family_name', '')

        # Find or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': given_name,
                'last_name': family_name,
            }
        )

        # Find or create social account
        social_account, _ = SocialAccount.objects.get_or_create(
            user=user,
            provider='google',
            defaults={'uid': google_id}
        )

        # Log the user in
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return JsonResponse({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )


@require_POST
def logout_view(request):
    """
    Logs out the current user
    """
    django_logout(request)
    return JsonResponse({
        "success": True,
        "message": "Logged out successfully"
    })