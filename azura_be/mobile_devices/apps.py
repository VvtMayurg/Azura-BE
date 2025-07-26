from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MobileDevicesConfig(AppConfig):
    name = "azura_be.mobile_devices"
    verbose_name = _("Mobile Devices")
