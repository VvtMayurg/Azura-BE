from django.conf import settings
from django.db import connection
from django.http import HttpResponseForbidden
from django.urls import set_urlconf
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name
from django_tenants.utils import get_public_schema_urlconf
from django_tenants.utils import get_tenant_types
from django_tenants.utils import has_multi_type_tenants

from digimedix_be.organizations.models import Organization

class OrganizationMainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith(settings.ADMIN_URL):
            return None

        connection.set_schema_to_public()
        request.organization = None
        org_name = request.headers.get("X-Header", "").strip()
        if not org_name:
            return None

        organization = Organization.objects.filter(name__iexact=org_name).first()
        if organization is None:
            return HttpResponseForbidden(content="Please provide correct organization")
        request.organization = organization
        connection.set_tenant(request.organization)
        return self.setup_url_routing(request=request, force_public=False)

    @staticmethod
    def setup_url_routing(request, force_public):
        public_schema_name = get_public_schema_name()
        if has_multi_type_tenants():
            tenant_types = get_tenant_types()
            if not hasattr(request, "tenant") or ((force_public or request.organization.schema_name == get_public_schema_name()) and "URLCONF" in tenant_types[public_schema_name]):
                request.urlconf = get_public_schema_urlconf()
            else:
                tenant_type = request.organization.get_tenant_type()
                request.urlconf = tenant_types[tenant_type]["URLCONF"]
            set_urlconf(request.urlconf)
        # Do we have a public-specific urlconf?
        elif hasattr(settings, "PUBLIC_SCHEMA_URLCONF") and (force_public or request.organization.schema_name == get_public_schema_name()):
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
