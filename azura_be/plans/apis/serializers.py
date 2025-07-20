from rest_framework import serializers

from azura_be.core.apis.serializers import CategorySerializer, ConditionRelatedSerializer, FlagSerializer, FrequencySerializer, TagSerializer, ICDCodeSerializer
from azura_be.plans.models import Form, Plan


class FormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ("title", "tags", "flag", "frequency", "conditions", "category", "comment", "nas", "questions")



class FormSerializer(serializers.ModelSerializer):
    conditions = ConditionRelatedSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    frequency = FrequencySerializer(required=False)
    category = CategorySerializer(required=False)
    flag = FlagSerializer(required=False)

    class Meta:
        model = Form
        fields = "__all__"


class PlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("programs", "name", "conditions", "icd_codes", "goals", "barriers", "symptoms", "interventions", "number_to_tracks", "expected_outcomes", "supports", "allergies", "medications")


class PlanSerializer(serializers.ModelSerializer):
    conditions = ConditionRelatedSerializer(many=True, required=False)
    icd_codes = ICDCodeSerializer(many=True, required=False)
    
    class Meta:
        model = Plan
        fields = "__all__"
