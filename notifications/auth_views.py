from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile, Trigger
from .services.notification_dispatcher import dispatch_notification

User = get_user_model()


def fire_user_notification(event_type, user):
    try:
        trigger = Trigger.objects.filter(
            event_type=event_type,
            is_active=True,
        ).first()

        if not trigger:
            return {"message": "Trigger is not configured or inactive."}

        return dispatch_notification(trigger, user)

    except Exception as error:
        # Notification failure should not block login or logout.
        return {
            "message": "Authentication successful, but notification processing failed.",
            "error": str(error),
        }


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    username = request.data.get("username", "").strip()
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")
    whatsapp_phone = request.data.get("whatsapp_phone", "").strip()

    if not username or not email or not password or not whatsapp_phone:
        return Response(
            {"error": "Username, email, password and WhatsApp number are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    UserProfile.objects.create(
        user=user,
        whatsapp_phone=whatsapp_phone,
    )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "message": "Registration successful.",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "whatsapp_phone": whatsapp_phone,
                "is_staff": user.is_staff,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)

    notification_result = fire_user_notification("login", user)

    profile = getattr(user, "profile", None)

    return Response(
        {
            "message": "Login successful.",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "whatsapp_phone": profile.whatsapp_phone if profile else "",
                "is_staff": user.is_staff,
            },
            "notifications": notification_result,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    notification_result = fire_user_notification("logout", request.user)

    request.user.auth_token.delete()

    return Response(
        {
            "message": "Logout successful.",
            "notifications": notification_result,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    profile = getattr(user, "profile", None)

    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "whatsapp_phone": profile.whatsapp_phone if profile else "",
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
    )