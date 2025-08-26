import base64
from urllib.parse import urljoin

import requests
from django.conf import settings

RESOURCE_PATH_MAPPING = {
    "service_code": "/api/v2//service_codes/",
    "diagnostic_codes": "/api/v2//diagnostic_codes/",
    "ontario_master_numbers": "/api/v2//ontario_master_numbers/%s/",
    "calculate_values": "/api/v2/invoice/calculate_values/",
}


class GovernmentBillingService:
    def __init__(self):
        self.base_url = settings.BILLING_BASE_URL
        self.username = settings.BILLING_USERNAME
        self.password = settings.BILLING_PASSWORD

    def _get_headers(self):
        encoded = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return {
            "Authorization": f"Basic {encoded}",
        }

    def _build_url(self, resource, path_args=None):
        path = RESOURCE_PATH_MAPPING.get(resource) % path_args if path_args else RESOURCE_PATH_MAPPING.get(resource)
        return urljoin(self.base_url, path)

    def execute(self, method, resource, params=None, data=None, path_args=None):
        headers = self._get_headers()
        url = self._build_url(resource, path_args)

        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            response = requests.get(url, params=params, headers=headers, timeout=10)

        return response.json()
