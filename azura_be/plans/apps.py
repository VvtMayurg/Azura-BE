from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlansConfig(AppConfig):
    name = "azura_be.plans"
    verbose_name = _("Plans")
