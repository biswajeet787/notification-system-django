
from django.conf import settings
from django.http import JsonResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trigger, NotificationTemplate, PushSubscription
from .serializers import (
    TriggerSerializer,
    NotificationTemplateSerializer,
    PushSubscriptionSerializer,
)
from .services.template_renderer import render_template


# Health Check
def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "message": "Notification API is running successfully"
    })


# Trigger ViewSet
class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.prefetch_related("templates").all()
    serializer_class = TriggerSerializer

    @action(detail=True, methods=["post"])
    def fire(self, request, pk=None):

        trigger = self.get_object()

        if not trigger.is_active:
            return Response(
                {"message": "This trigger is inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get user details
        user_data = request.data.get("user") or {}

        name = (
            user_data.get("name")
            or request.data.get("full_name")
            or request.data.get("user_name")
            or "Test User"
        )

        email = (
            user_data.get("email")
            or request.data.get("email")
            or request.data.get("recipient_email")
        )

        phone = (
            user_data.get("phone")
            or user_data.get("whatsapp_phone")
            or request.data.get("whatsapp_phone")
            or request.data.get("recipient_phone")
        )

        # Template context
        context = {
            "user": {
                "name": name,
                "email": email,
                "phone": phone,
            }
        }

        enabled_templates = trigger.templates.filter(
            is_enabled=True
        )

        delivery_results = []

        # Send notifications through enabled channels
        for template in enabled_templates:

            try:

                # EMAIL
                if template.channel == "email":

                    from .services.email_service import (
                        send_notification_email
                    )

                    if not email:
                        raise ValueError(
                            "User email is required."
                        )

                    sent = send_notification_email(
                        recipient_email=email,
                        subject=template.subject or template.name,
                        message=template.body,
                        variable_mapping=template.variable_mapping,
                        context=context,
                    )

                    result = {
                        "success": sent,
                        "message": (
                            "Email sent successfully."
                            if sent
                            else "Email was not sent."
                        ),
                    }

                # WHATSAPP
                elif template.channel == "whatsapp":

                    from .services.whatsapp_service import (
                        send_whatsapp_notification
                    )

                    if not phone:
                        raise ValueError(
                            "WhatsApp phone number is required."
                        )

                    provider_response = send_whatsapp_notification(
                        recipient_phone=phone,
                        message=template.body,
                        variable_mapping=template.variable_mapping,
                        context=context,
                    )

                    result = {
                        "success": True,
                        "message": "WhatsApp request accepted.",
                        "provider_response": provider_response,
                    }

                # WEB PUSH
                elif template.channel == "web_push":

                    from .services.web_push_service import (
                        send_web_push_notification
                    )

                    title = render_template(
                        template.subject or template.name,
                        template.variable_mapping,
                        context,
                    )

                    body = render_template(
                        template.body,
                        template.variable_mapping,
                        context,
                    )

                    subscriptions = PushSubscription.objects.filter(
                        is_active=True
                    )

                    if not subscriptions.exists():
                        raise ValueError(
                            "No active browser subscriptions found."
                        )

                    push_results = []

                    for subscription in subscriptions:

                        subscription_info = {
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.p256dh,
                                "auth": subscription.auth,
                            },
                        }

                        push_result = send_web_push_notification(
                            subscription_info=subscription_info,
                            title=title,
                            message=body,
                        )

                        push_results.append(push_result)

                    result = {
                        "success": True,
                        "message": "Web Push notifications accepted.",
                        "subscriptions": len(push_results),
                    }

                else:
                    raise ValueError(
                        f"Unsupported channel: {template.channel}"
                    )

                delivery_results.append({
                    "channel": template.channel,
                    "template_id": template.id,
                    "template_name": template.name,
                    **result,
                })

            except Exception as error:

                delivery_results.append({
                    "channel": template.channel,
                    "template_id": template.id,
                    "template_name": template.name,
                    "success": False,
                    "error": str(error),
                })

        # Calculate delivery results
        successful = sum(
            1
            for item in delivery_results
            if item["success"]
        )

        failed = len(delivery_results) - successful

        return Response({
            "message": "Notification event processed.",
            "trigger": trigger.name,
            "event_type": trigger.event_type,
            "total_enabled_channels": len(delivery_results),
            "successful_deliveries": successful,
            "failed_deliveries": failed,
            "notifications": delivery_results,
            "delivery_status": (
                "success"
                if successful == len(delivery_results)
                else "partial_or_failed"
            ),
        })


# Notification Template ViewSet
class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.select_related(
        "trigger"
    ).all()

    serializer_class = NotificationTemplateSerializer

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):

        template = self.get_object()

        if not template.is_enabled:
            return Response(
                {
                    "error": "This notification template is disabled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        context = {
            "user": {
                "name": request.data.get(
                    "user_name",
                    "Test User"
                )
            }
        }

        try:

            # EMAIL TEST
            if template.channel == "email":

                from .services.email_service import (
                    send_notification_email
                )

                recipient = request.data.get("recipient_email")

                if not recipient:
                    return Response(
                        {"error": "recipient_email is required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                sent = send_notification_email(
                    recipient_email=recipient,
                    subject=template.subject or template.name,
                    message=template.body,
                    variable_mapping=template.variable_mapping,
                    context=context,
                )

                return Response({
                    "message": "Test email sent successfully.",
                    "template_id": template.id,
                    "sent": sent,
                })

            # WHATSAPP TEST
            elif template.channel == "whatsapp":

                from .services.whatsapp_service import (
                    send_whatsapp_notification
                )

                recipient = request.data.get("recipient_phone")

                if not recipient:
                    return Response(
                        {"error": "recipient_phone is required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                result = send_whatsapp_notification(
                    recipient_phone=recipient,
                    message=template.body,
                    variable_mapping=template.variable_mapping,
                    context=context,
                )

                return Response({
                    "message": "WhatsApp message request accepted.",
                    "template_id": template.id,
                    "sent": True,
                    "provider_response": result,
                })

            return Response({
                "message": (
                    "Delivery is not implemented for this channel yet."
                ),
                "template_id": template.id,
                "channel": template.channel,
                "sent": False,
            })

        except Exception as error:

            return Response({
                "message": "Notification delivery failed.",
                "error": str(error),
                "sent": False,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Push Subscription ViewSet
class PushSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PushSubscription.objects.all()
    serializer_class = PushSubscriptionSerializer

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):

        subscription = self.get_object()

        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth,
            },
        }

        try:

            from .services.web_push_service import (
                send_web_push_notification
            )

            result = send_web_push_notification(
                subscription_info=subscription_info,
                title="Notification Management System",
                message="Your Web Push notification is working!",
            )

            return Response({
                "message": "Push notification request accepted.",
                "result": result,
            })

        except Exception as error:

            return Response({
                "message": "Push notification failed.",
                "error": str(error),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# VAPID Public Key
def vapid_public_key(request):
    return JsonResponse({
        "publicKey": settings.VAPID_PUBLIC_KEY
    })
