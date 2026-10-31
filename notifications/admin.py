from django.contrib import admin
from .models import NotificationTemplate, Trigger

class NotificationTemplateInline(admin.TabularInline):
    model = NotificationTemplate
    extra = 0

@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ("name", "event_type", "is_active", "updated_at")
    list_filter = ("is_active", "event_type")
    search_fields = ("name", "description")
    inlines = [NotificationTemplateInline]

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "trigger", "channel", "is_enabled", "updated_at")
    list_filter = ("channel", "is_enabled")
    search_fields = ("name", "body", "trigger__name")
