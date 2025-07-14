from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BusinessAccountsConfig(AppConfig):
    name = "azura_be.business_accounts"
    verbose_name = _("Business Accounts")
