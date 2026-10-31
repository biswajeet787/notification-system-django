
from rest_framework import serializers

from .models import Trigger, NotificationTemplate, PushSubscription

class NotificationTemplateSerializer(serializers.ModelSerializer):
    channel_display = serializers.CharField(
        source="get_channel_display",
        read_only=True
    )

    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class TriggerSerializer(serializers.ModelSerializer):
    templates = NotificationTemplateSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Trigger
        fields = [
            "id",
            "name",
            "event_type",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "templates",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]



class PushSubscriptionSerializer(serializers.ModelSerializer):
    endpoint = serializers.URLField(validators=[])

    class Meta:
        model = PushSubscription
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user_id"]
