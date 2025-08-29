from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from azura_be.business_accounts.models import BusinessAccount
from azura_be.business_accounts.models import EnabledDomain

admin.site.register(EnabledDomain)


@admin.register(BusinessAccount)
class BusinessAccountAdmin(TenantAdminMixin, admin.ModelAdmin):
    change_form_template = "django_tenants/tenant/change_form.html"
    list_display = (
        "id",
        "name",
    )
