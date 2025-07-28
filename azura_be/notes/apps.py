from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotesConfig(AppConfig):
    name = "azura_be.notes"
    verbose_name = _("Notes")
