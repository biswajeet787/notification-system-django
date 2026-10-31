import base64
import json

from django.conf import settings
from pywebpush import webpush, WebPushException


def send_web_push_notification(subscription_info, title, message):
    encoded_key = "".join(settings.VAPID_PRIVATE_KEY.split())
    encoded_key += "=" * (-len(encoded_key) % 4)

    pem_key = base64.b64decode(encoded_key)

    # Save decoded PEM key as a file
    key_path = settings.BASE_DIR / "vapid_private.pem"
    key_path.write_bytes(pem_key)

    try:
        response = webpush(
            subscription_info=subscription_info,
            data=json.dumps({
                "title": title,
                "body": message,
            }),
            vapid_private_key=str(key_path),
            vapid_claims={
                "sub": settings.VAPID_CLAIMS_EMAIL,
            },
        )

        return {
            "success": True,
            "status_code": response.status_code,
        }

    except WebPushException as error:
        raise Exception(
            f"Web Push delivery failed: {error}"
        ) from error