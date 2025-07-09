from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProviderGroupsConfig(AppConfig):
    name = "azura_be.provider_groups"
    verbose_name = _("Provider Groups")
