import django_filters
from azura_be.tasks.models import Task

class TaskFilter(django_filters.FilterSet):
    reason = django_filters.CharFilter(
        field_name="reason", 
        lookup_expr="icontains", 
        label="Reason", 
        required=False
        )
    description = django_filters.CharFilter(
        field_name="description", 
        lookup_expr="icontains", 
        label="Description", 
        required=False
        )

    priority = django_filters.ChoiceFilter(
        field_name="priority",
        choices=Task._meta.get_field("priority").choices,
        label="Priority",
        required=False,
        )
    completed = django_filters.BooleanFilter(
        field_name="completed", 
        label="Completed", 
        required=False
        )

    patient_id = django_filters.NumberFilter(
        field_name="patient__id", 
        label="Patient ID", 
        required=False
        )
    user_id = django_filters.NumberFilter(
        field_name="user__id", 
        label="User ID", 
        required=False
        )
    due_after = django_filters.DateTimeFilter(
        field_name="due_at", 
        lookup_expr="gte", 
        label="Due After", 
        required=False
        )
    due_before = django_filters.DateTimeFilter(
        field_name="due_at", 
        lookup_expr="lte", 
        label="Due Before", 
        required=False
        )
    completed_after = django_filters.DateTimeFilter(
        field_name="completed_at", 
        lookup_expr="gte", 
        label="Completed After", 
        required=False
        )
    completed_before = django_filters.DateTimeFilter(
        field_name="completed_at", 
        lookup_expr="lte", 
        label="Completed Before", 
        required=False
        )

    class Meta:
        model = Task
        fields = [
            "reason",
            "description",
            "priority",
            "completed",
            "patient_id",
            "user_id",
            "due_after",
            "due_before",
            "completed_after",
            "completed_before",
        ]
        