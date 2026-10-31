
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TriggerViewSet,
    NotificationTemplateViewSet,
    PushSubscriptionViewSet,
    health_check,
    vapid_public_key,
)

router = DefaultRouter()

router.register(
    "triggers",
    TriggerViewSet,
    basename="trigger"
)

router.register(
    "templates",
    NotificationTemplateViewSet,
    basename="template"
)

router.register("push-subscriptions", PushSubscriptionViewSet)

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("", include(router.urls)),
    path(
    "web-push/public-key/",
    vapid_public_key,
    name="web-push-public-key",
),
]
