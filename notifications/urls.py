from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TriggerViewSet,
    NotificationTemplateViewSet,
    PushSubscriptionViewSet,
    health_check,
    vapid_public_key,
)

from .auth_views import (
    register,
    login,
    logout,
    current_user,
)

router = DefaultRouter()
router.register("triggers", TriggerViewSet, basename="trigger")
router.register("templates", NotificationTemplateViewSet, basename="template")
router.register(
    "push-subscriptions",
    PushSubscriptionViewSet,
    basename="push-subscription",
)

urlpatterns = [
    path("health/", health_check, name="health-check"),

    # Authentication
    path("auth/register/", register, name="register"),
    path("auth/login/", login, name="login"),
    path("auth/logout/", logout, name="logout"),
    path("auth/me/", current_user, name="current-user"),

    # Notification APIs
    path("", include(router.urls)),

    # Web Push
    path("web-push/public-key/", vapid_public_key, name="web-push-public-key"),
]