from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "digimedix_be.core"
    verbose_name = _("Core")
