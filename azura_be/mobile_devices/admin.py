from django.contrib import admin
from django.contrib.auth import get_user_model
from django_otp.admin import user_model_search_fields

from azura_be.mobile_devices.models import MobileDevice

User = get_user_model()


def _search_fields():
    candidate_search_field = [User.USERNAME_FIELD, "email"]

    search_fields, search_help_text = user_model_search_fields(candidate_search_field)
    search_fields += ["email"]

    return search_fields, search_help_text


@admin.register(MobileDevice)
class MobileDeviceAdmin(admin.ModelAdmin):
    """
    :class:`~django.contrib.admin.ModelAdmin` for
    :class:`~azura_be.mobile_devices.models.MobileDevice`.
    """

    list_display = ["user", "name", "created_at", "last_used_at", "confirmed"]
    list_filter = ["created_at", "last_used_at", "confirmed"]

    raw_id_fields = ["user"]
    readonly_fields = ["created_at", "last_used_at"]
    search_fields, search_help_text = _search_fields()

    fieldsets = [
        (
            "Identity",
            {
                "fields": ["user", "name", "confirmed"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "last_used_at"],
            },
        ),
    ]
