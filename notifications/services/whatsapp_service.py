import re
import requests
from django.conf import settings

from .template_renderer import render_template


def send_whatsapp_notification(
    recipient_phone,
    message,
    variable_mapping=None,
    context=None,
):
    access_token = settings.WHATSAPP_ACCESS_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    api_version = settings.WHATSAPP_API_VERSION

    if not access_token or not phone_number_id or not api_version:
        raise ValueError("WhatsApp API credentials are not configured.")

    rendered_message = render_template(
        message,
        variable_mapping,
        context,
    )

    recipient = re.sub(r"\D", "", recipient_phone)

    if not recipient:
        raise ValueError("A valid recipient phone number is required.")

    url = (
        f"https://graph.facebook.com/"
        f"{api_version}/{phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": rendered_message,
        },
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()