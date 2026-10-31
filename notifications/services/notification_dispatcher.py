from .template_renderer import render_template
from ..models import PushSubscription


def dispatch_notification(trigger, user):
    if not trigger.is_active:
        return {
            "message": "Trigger is inactive.",
            "notifications": [],
        }

    profile = getattr(user, "profile", None)

    context = {
        "user": {
            "name": user.username,
            "email": user.email,
            "phone": profile.whatsapp_phone if profile else "",
        }
    }

    results = []

    templates = trigger.templates.filter(is_enabled=True)

    for template in templates:
        try:
            if template.channel == "email":
                from .email_service import send_notification_email

                if not user.email:
                    raise ValueError("User email is required.")

                subject = render_template(
                    template.subject or template.name,
                    template.variable_mapping,
                    context,
                )

                sent = send_notification_email(
                    recipient_email=user.email,
                    subject=subject,
                    message=template.body,
                    variable_mapping=template.variable_mapping,
                    context=context,
                )

                results.append({
                    "channel": "email",
                    "success": sent,
                })

            elif template.channel == "whatsapp":
                from .whatsapp_service import send_whatsapp_notification

                if not profile or not profile.whatsapp_phone:
                    raise ValueError("User WhatsApp number is required.")

                response = send_whatsapp_notification(
                    recipient_phone=profile.whatsapp_phone,
                    message=template.body,
                    variable_mapping=template.variable_mapping,
                    context=context,
                )

                results.append({
                    "channel": "whatsapp",
                    "success": True,
                    "provider_response": response,
                })

            elif template.channel == "web_push":
                from .web_push_service import send_web_push_notification

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
                    user_id=str(user.id),
                    is_active=True,
                )

                if not subscriptions.exists():
                    raise ValueError("No active browser subscriptions found.")

                for subscription in subscriptions:
                    subscription_info = {
                        "endpoint": subscription.endpoint,
                        "keys": {
                            "p256dh": subscription.p256dh,
                            "auth": subscription.auth,
                        },
                    }

                    send_web_push_notification(
                        subscription_info=subscription_info,
                        title=title,
                        message=body,
                    )

                results.append({
                    "channel": "web_push",
                    "success": True,
                    "subscriptions": subscriptions.count(),
                })

        except Exception as error:
            results.append({
                "channel": template.channel,
                "success": False,
                "error": str(error),
            })

    successful = sum(
        1 for item in results if item["success"]
    )

    return {
        "trigger": trigger.name,
        "successful_deliveries": successful,
        "failed_deliveries": len(results) - successful,
        "notifications": results,
    }