from django.db import models
from django.conf import settings

class Trigger(models.Model):
    class EventType(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        INACTIVE_1_DAY = "inactive_1_day", "Inactive for 1 day"
        INACTIVE_1_WEEK = "inactive_1_week", "Inactive for 1 week"
        PASSWORD_RESET = "password_reset", "Password reset"
        ORDER_PLACED = "order_placed", "Order placed"

    name = models.CharField(max_length=120)
    event_type = models.CharField(max_length=40, choices=EventType.choices, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

class NotificationTemplate(models.Model):
    class Channel(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "Email"
        WEB_PUSH = "web_push", "Web Push"

    trigger = models.ForeignKey(Trigger, related_name="templates", on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_enabled = models.BooleanField(default=True)
    variable_mapping = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["trigger_id", "channel"]
        constraints = [models.UniqueConstraint(fields=["trigger", "channel"], name="unique_template_per_trigger_channel")]

    def __str__(self):
        return f"{self.trigger.name} — {self.get_channel_display()}"


class PushSubscription(models.Model):
    user_id = models.CharField(max_length=100, blank=True, null=True)
    endpoint = models.URLField(max_length=1000, unique=True)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Push Subscription - {self.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    whatsapp_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return f"Profile - {self.user.username}"