from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from azura_be.business_accounts.models import BusinessAccount
from azura_be.business_accounts.models import EnabledDomain

admin.site.register(EnabledDomain)


@admin.register(BusinessAccount)
class BusinessAccountAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
