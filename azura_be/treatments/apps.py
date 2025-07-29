from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TreatmentsConfig(AppConfig):
    name = "azura_be.treatments"
    verbose_name = _("Treatments")
