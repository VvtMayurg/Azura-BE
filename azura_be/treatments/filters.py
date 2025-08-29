import django_filters
from azura_be.treatments.models import PatientTreatmentPlan, PatientTreatmentPlanResponse,PatientForm, PatientFormResponse

class PatientTreatmentPlanFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(
        field_name="patient__id",
        label='Patient',
        required=False
        )
    plan = django_filters.NumberFilter(
        field_name="plan__id",
        label='Plan',
        required=False
        )
    active = django_filters.BooleanFilter(
        field_name='active',
        label='Active',
        required=False)

    class Meta:
        model = PatientTreatmentPlan
        fields = ["patient", "plan", "active"]

class PatientTreatmentPlanResponseFilter(django_filters.FilterSet):
    treatment_plan = django_filters.NumberFilter(
        field_name="treatment_plan__id",
        label='Treatment_plan'
        )

    class Meta:
        model = PatientTreatmentPlanResponse
        fields = ["treatment_plan"]

class PatientFormFilter(django_filters.FilterSet):
    patient_id = django_filters.NumberFilter(
        field_name="patient__id", 
        lookup_expr="exact",
        required=False
        )
    form_id = django_filters.NumberFilter(
        field_name="form__id", 
        lookup_expr="exact",
        required=False
        )
    active = django_filters.BooleanFilter(
        field_name="active",
        required=False
        )

    class Meta:
        model = PatientForm
        fields = ["patient", "form", "active"]

class PatientFormResponseFilter(django_filters.FilterSet):
    patient_form_id = django_filters.NumberFilter(
        field_name="patient_form__id", 
        lookup_expr="exact",
        required=False
        )
    response_contains = django_filters.CharFilter(
        field_name="response", 
        lookup_expr="icontains",
        required=False)  

    class Meta:
        model = PatientFormResponse
        fields = ["patient_form", "response"]
