from django.utils import timezone

from azura_be.appointments.apis.serializers import AppointmentSerializer
from azura_be.appointments.models import Appointment
from azura_be.appointments.models import Encounter
from azura_be.base.constants import AppointmentStatusChoices
from azura_be.base.constants import EncounterStatusChoice
from azura_be.business_accounts.models import CommunicationTemplate
from azura_be.clinical.models import LabResult
from azura_be.communications.apis.serializers import ThreadMessageSerializer
from azura_be.communications.models import ThreadMessage
from azura_be.core.models import Specialty
from azura_be.locations.models import Location
from azura_be.patients.models import Patient
from azura_be.plans.models import Form
from azura_be.provider_groups.models import Department
from azura_be.provider_groups.models import ProviderGroup
from azura_be.tasks.apis.serializers import TaskSerializer
from azura_be.tasks.models import Task
from azura_be.users.models import User


def provider_dashboard_stats(user):
    today = timezone.now()

    return {
        "lab_results": LabResult.objects.all().count(),
        "tasks": Task.objects.filter(user=user).count(),
        "unsigned_encounter": Encounter.objects.filter(user=user)
        .exclude(status__in=[EncounterStatusChoice.CANCELLED, EncounterStatusChoice.COMPLETED])
        .count(),
        "claim_received": 1,
        "claim_in_progress": 1,
        "claim_requiring_action": 1,
        "appointments": {
            "scheduled": Appointment.objects.filter(user=user, status=AppointmentStatusChoices.SCHEDULED).count(),
            "cancelled": Appointment.objects.filter(user=user, status=AppointmentStatusChoices.CANCELLED).count(),
            "not_show": Appointment.objects.filter(user=user, status=AppointmentStatusChoices.NOT_SHOW).count(),
            "declined": Appointment.objects.filter(user=user, status=AppointmentStatusChoices.DECLINED).count(),
        },
        "upcoming_appointments": AppointmentSerializer(
            Appointment.objects.filter(user=user, status=AppointmentStatusChoices.SCHEDULED, start_at__date__gte=today),
            many=True,
        ).data,
        "todo_tasks": TaskSerializer(Task.objects.filter(user=user, due_at__date=today, completed=False), many=True),
        "chat": ThreadMessageSerializer(ThreadMessage.objects.filter(thread__thread_users__user=user, read=False).exclude(user=user), many=True).data,
    }


def admin_dashboard_stats(user):
    provider_groups = ProviderGroup.objects.all().count()
    locations = Location.objects.all().count()
    departments = Department.objects.all().count()
    specialties = Specialty.objects.all().count()
    organization_users = User.objects.filter(is_provider=False).count()
    users = User.objects.all().count()

    return {
        "total_patients": Patient.objects.all().count(),
        "healthcare_providers": User.objects.all(is_provider=True).count(),
        "monthly_revenue": 1,
        "system_uptime": 1,
        "overview": {
            "provider_groups": provider_groups,
            "locations": locations,
            "departments": departments,
            "specialties": specialties,
            "users": users,
            "organization_users": organization_users,
        },
        "all_modules": {
            "provider_groups": provider_groups,
            "locations": locations,
            "departments": departments,
            "specialties": specialties,
            "organization_users": organization_users,
            "form_builders": Form.objects.all().count(),
            "custom_forms": 1,
            "form_templates": 1,
            "email_sms_templates": CommunicationTemplate.objects.all().count(),
            "coding_management": 1,
            "audit_logs": 1,
            "billing_payments": 1,
            "subscription_plans": 1,
            "user_profiles": users,
            "configurations": 1,
        },
        "analytics": {
            "age_distribution": {
                "under_18": 0,
                "above_18_under_25": 0,
                "above_36_under_55": 0,
                "above_56": 0,
            },
            "monthly_registrations": {
                "jan": 1,
                "feb": 1,
                "dec": 1,
            },
            "top_performing_providers": [{"id": "uuid", "name": "name", "patients": 1}],
            "patient_satisfaction": 1,
            "avg_consultation_time": "10 sec",
            "follow_up_rate": 1,
        },
        "audit_logs": [{}],
    }
