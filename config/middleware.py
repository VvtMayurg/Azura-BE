from django.conf import settings
from django.db import connection
from django.urls import set_urlconf
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name
from django_tenants.utils import get_public_schema_urlconf
from django_tenants.utils import get_tenant_types
from django_tenants.utils import has_multi_type_tenants

from azura_be.business_accounts.models import BusinessAccount


class BusinessAccountMainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith(settings.ADMIN_URL) or request.path.startswith("/api/auth/"):
            return None

        connection.set_schema_to_public()
        request.business_account = None
        origin = request.headers.get("Origin")

        business_account = BusinessAccount.objects.filter(
            web_address__iexact=origin,
        ).first()
        if business_account is None:
            return None
        request.business_account = business_account
        connection.set_tenant(request.business_account)
        return self.setup_url_routing(request=request, force_public=False)

    @staticmethod
    def setup_url_routing(request, force_public):
        public_schema_name = get_public_schema_name()
        if has_multi_type_tenants():
            tenant_types = get_tenant_types()
            if not hasattr(request, "tenant") or (
                (force_public or request.business_account.schema_name == get_public_schema_name()) and "URLCONF" in tenant_types[public_schema_name]
            ):
                request.urlconf = get_public_schema_urlconf()
            else:
                tenant_type = request.business_account.get_tenant_type()
                request.urlconf = tenant_types[tenant_type]["URLCONF"]
            set_urlconf(request.urlconf)
        # Do we have a public-specific urlconf?
        elif hasattr(settings, "PUBLIC_SCHEMA_URLCONF") and (force_public or request.business_account.schema_name == get_public_schema_name()):
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
