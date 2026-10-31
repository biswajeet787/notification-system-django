from django.core.management.base import BaseCommand
from notifications.models import NotificationTemplate, Trigger

class Command(BaseCommand):
    help = "Create demo Login and Logout triggers with templates for all three channels."

    def handle(self, *args, **options):
        demo = [
            ("User Login", Trigger.EventType.LOGIN, "Triggered when a user logs in.", {
                "whatsapp": ("Login WhatsApp", "", "Welcome back, {{name}}!"),
                "email": ("Login Email", "Welcome back!", "Hello {{name}}, you have successfully logged in."),
                "web_push": ("Login Web Push", "", "Welcome back to your account."),
            }),
            ("User Logout", Trigger.EventType.LOGOUT, "Triggered when a user logs out.", {
                "whatsapp": ("Logout WhatsApp", "", "Goodbye {{name}}. You have logged out."),
                "email": ("Logout Email", "You have logged out", "Hello {{name}}, you have successfully logged out."),
                "web_push": ("Logout Web Push", "", "You have logged out successfully."),
            }),
        ]
        for name, event_type, description, templates in demo:
            trigger, _ = Trigger.objects.update_or_create(
                event_type=event_type,
                defaults={"name": name, "description": description, "is_active": True},
            )
            for channel, (template_name, subject, body) in templates.items():
                NotificationTemplate.objects.update_or_create(
                    trigger=trigger,
                    channel=channel,
                    defaults={"name": template_name, "subject": subject, "body": body,
                              "is_enabled": True, "variable_mapping": {"name": "user.name"}},
                )
        self.stdout.write(self.style.SUCCESS("Demo triggers and templates created."))
