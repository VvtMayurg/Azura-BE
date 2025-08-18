from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatientPortalConfig(AppConfig):
    name = "azura_be.patient_portal"
    verbose_name = _("Patient Portal")
