
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings

from .template_renderer import render_template


BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_notification_email(
    recipient_email,
    subject,
    message,
    variable_mapping=None,
    context=None,
):
    api_key = getattr(settings, "BREVO_API_KEY", "")
    sender_email = getattr(settings, "BREVO_SENDER_EMAIL", "")
    sender_name = getattr(
        settings,
        "BREVO_SENDER_NAME",
        "Notification System",
    )

    if not api_key:
        raise ValueError("Brevo API key is not configured.")

    if not sender_email:
        raise ValueError("Brevo sender email is not configured.")

    rendered_subject = render_template(
        subject,
        variable_mapping,
        context,
    )

    rendered_message = render_template(
        message,
        variable_mapping,
        context,
    )

    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email,
        },
        "to": [
            {
                "email": recipient_email,
            }
        ],
        "subject": rendered_subject,
        "textContent": rendered_message,
    }

    request = Request(
        BREVO_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))

            print("Brevo email accepted:", result.get("messageId"))

            return True

    except HTTPError as error:
        error_details = error.read().decode("utf-8")

        raise Exception(
            f"Brevo email API error ({error.code}): {error_details}"
        ) from error

    except URLError as error:
        raise Exception(
            f"Unable to connect to Brevo: {error.reason}"
        ) from error
