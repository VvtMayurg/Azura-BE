from django.utils import timezone

from azura_be.appointments.apis.serializers import AppointmentSerializer
from azura_be.appointments.models import Appointment
from azura_be.base.constants import AppointmentStatusChoices
from azura_be.clinical.apis.serializers import MedicationSerializer
from azura_be.clinical.models import LabResult
from azura_be.clinical.models import Medication
from azura_be.communications.apis.serializers import ThreadMessageSerializer
from azura_be.communications.models import ThreadMessage


def patient_dashboard(patient):
    today = timezone.now().date()

    return {
        "appointments": {
            "scheduled": Appointment.objects.filter(patient=patient, status=AppointmentStatusChoices.SCHEDULED).count(),
            "cancelled": Appointment.objects.filter(patient=patient, status=AppointmentStatusChoices.CANCELLED).count(),
            "not_show": Appointment.objects.filter(patient=patient, status=AppointmentStatusChoices.NOT_SHOW).count(),
            "declined": Appointment.objects.filter(patient=patient, status=AppointmentStatusChoices.DECLINED).count(),
        },
        "upcoming_appointments": AppointmentSerializer(Appointment.objects.filter(patient=patient, start_at__date__gte=today), many=True).data,
        "lab_results": LabResult.objects.filter(patient=patient).count(),
        "medication": MedicationSerializer(Medication.objects.filter(patient=patient), many=True).data,
        "chat": ThreadMessageSerializer(
            ThreadMessage.objects.filter(thread__thread_users__user=patient.user, read=False).exclude(user=patient.user),
            many=True,
        ).data,
    }
