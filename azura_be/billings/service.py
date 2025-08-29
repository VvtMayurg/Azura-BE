import base64
from urllib.parse import urljoin

import requests
from django.conf import settings

from azura_be.patients.models import Patient
from azura_be.users.models import User

RESOURCE_PATH_MAPPING = {
    "service_code": "/api/v2//service_codes/",
    "diagnostic_codes": "/api/v2//diagnostic_codes/",
    "ontario_master_numbers": "/api/v2//ontario_master_numbers/%s/",
    "calculate_values": "/api/v2/invoice/calculate_values/",
    "eligibility_check": "/api/v2/patient/service_code/eligibility/",
    "eligibility": "/api/v2/patient/eligibility/",
    "create_invoice": "/api/v2/full_invoices/?duplicate_invoice_validation=false",
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

    def payload_for_invoice(
        self,
        patient: Patient,
        provider: User,
        billing_data,
        appointment_time,
    ):
        return {
            "patient": {
                "unique_id": str(patient.id),
                "salutation": "Mr" if patient.gender == "MALE" else "Ms",
                "first_name": patient.first_name,
                "middle_name": patient.middle_name,
                "last_name": patient.last_name,
                "health_number": patient.health_number,
                "ontario_version_code": "AB",
                "guardian_health_number": patient.guardian_health_number,
                "province_code": "ON",
                "birth_date": patient.date_of_birth.strftime("%Y-%m-%d"),
                "gender": patient.gender[0],
                "street_address_1": (patient.address or {}).get("address_1"),
                "street_address_2": (patient.address or {}).get("address_2"),
                "postal_code": (patient.address or {}).get("postal_code"),
                "city": (patient.address or {}).get("city"),
                "address_province_code": (patient.address or {}).get("province"),
                "country_code": (patient.address or {}).get("country"),
                "default_service_code": "03.03a",
                "default_diagnostic_code": "250",
                "default_admission_date": "2021-01-01",
                "phone_number_primary": patient.phone,
                "phone_number_cell": "1231231234",
                "phone_number_work": "1231231234",
                "referring_provider_number": "987654321",
                "referring_provider_province": "ON",
                "clinic_status": "active",
                "employer_name": "Work Tech",
                "employer_address": "100 Work Ave",
                "employer_city": "Ottawa",
                "employer_province_code": "ON",
                "employer_country": "CAN",
                "employer_phone": "1231231234",
            },
            "provider": {
                "unique_id": str(provider.uid),
                "first_name": provider.first_name,
                "last_name": provider.last_name,
                "practitioner_number": provider.practitioner_number,
                "ontario_group_number": provider.ontario_group_number,
            },
            "invoice": {
                "billing_type": "ontario",
                "appointment_timestamp": appointment_time,
                "chart_number": "C1234",
                "invoice_ontario_ohip_data": {
                    "health_number": patient.health_number,
                    "version_code": "WG",
                    "patient_birthdate": patient.date_of_birth.strftime("%Y-%m-%d"),
                    "payment_program": billing_data.get("payment_program", "N"),
                    "payee": billing_data.get("payee", "1"),
                    "referring_number": billing_data.get("referring_number"),
                    "master_number": billing_data.get("master_number"),
                    "admission_date": (patient.admission_date.strftime("%Y-%m-%d") if patient.admission_date else ""),
                    "referring_lab_number": "12345",
                    "manual_review_indicator": False,
                    "stale_dated_claim": False,
                    "service_location_indicator": "3821",
                    "registration_number": "",
                    "patient_last_name": "",
                    "patient_first_name": "",
                    "patient_gender": "",
                    "province_code": "",
                    "chart_number": "",
                    "office_notes": "",
                    "group_number_override": "",
                    "office_code_override": "",
                    "specialty_override": "",
                    "invoice_ontario_items": billing_data.get("service_data"),
                },
            },
            "auto_submit": False,
        }
