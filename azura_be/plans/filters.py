        
import django_filters
from azura_be.plans.models import Plan


class PlanFilter(django_filters.FilterSet):
    id=django_filters.NumberFilter(
        field_name='id',
        label='ID',
        required=False,
        lookup_expr="exact"
        )
    programs=django_filters.CharFilter(
        field_name='programs',
        label='Programs',
        required=False,
        lookup_expr="icontains"
        )
    name=django_filters.CharFilter(
        field_name='name',
        label='Name',
        required=False,
        lookup_expr="icontains"
        )
    conditions=django_filters.CharFilter(
        field_name='conditions',
        label='Conditions_Name',
        required=False,
        lookup_expr="icontains"
        )
    icd_codes=django_filters.CharFilter(
        field_name='icd_codes',
        label='icd_codes',
        required=False,
        lookup_expr="icontains"
        )
    
    class Meta:
        MOdel=Plan
        fields=[
            'id',
            'programs',
            'name',
            'conditions',
            'iccd_codes',
        ]


